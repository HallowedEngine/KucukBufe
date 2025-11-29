"""
BüfeOS - Production API (Multi-Tenant + Auth)
Online deployment için hazır
"""
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
import csv
import io
import os
from typing import List, Optional
from pydantic import BaseModel, EmailStr

# Production imports
from database_v2 import get_db, init_db, User, Product, Sale, StockAlert
from auth import get_current_active_user, hash_password, User as UserModel

# FastAPI app
app = FastAPI(
    title="BüfeOS API",
    description="Küçük büfeler için stok yönetim sistemi (Multi-Tenant)",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
app.mount("/templates", StaticFiles(directory=os.path.join(BASE_DIR, "templates"), html=True), name="templates")


# --- PYDANTIC MODELS ---

class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    bufe_adi: str
    telefon: Optional[str] = None
    adres: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class ProductCreate(BaseModel):
    name: str
    barcode: Optional[str] = None
    stock: int = 0
    cost_price: float = 0.0
    sell_price: float
    category: str = "Genel"


class SaleCreate(BaseModel):
    product_id: int
    quantity: int


# --- STARTUP ---

@app.on_event("startup")
def startup():
    """Uygulama başlarken DB'yi başlat"""
    init_db()
    print("🚀 BüfeOS v2.0 başlatıldı! (Multi-Tenant)")


# --- AUTHENTICATION ENDPOINTS ---

@app.post("/register")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Yeni kullanıcı kaydı (Ücretsiz deneme başlar)"""

    # Email zaten var mı?
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Bu email zaten kullanılıyor")

    # Username zaten var mı?
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Bu kullanıcı adı zaten kullanılıyor")

    # Yeni kullanıcı oluştur
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        bufe_adi=user_data.bufe_adi,
        telefon=user_data.telefon,
        adres=user_data.adres,
        is_trial=True,
        trial_ends_at=datetime.utcnow() + timedelta(days=30),  # 30 gün ücretsiz
        subscription_type="trial"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Kayıt başarılı! 30 gün ücretsiz deneme başladı.",
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "username": new_user.username,
            "bufe_adi": new_user.bufe_adi,
            "trial_ends_at": new_user.trial_ends_at
        }
    }


@app.get("/me")
def get_me(current_user: User = Depends(get_current_active_user)):
    """Mevcut kullanıcı bilgileri"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "bufe_adi": current_user.bufe_adi,
        "telefon": current_user.telefon,
        "is_trial": current_user.is_trial,
        "trial_ends_at": current_user.trial_ends_at,
        "subscription_type": current_user.subscription_type
    }


# --- DASHBOARD ENDPOINTS (Multi-Tenant) ---

@app.get("/dashboard/sales_today")
def get_sales_today(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Bugünkü satış özeti (Sadece kendi verisi)"""
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = today_start - timedelta(days=1)

    # Bugünkü satışlar (Sadece bu kullanıcının)
    today_sales = db.query(
        func.sum(Sale.total_price).label('revenue'),
        func.sum(Sale.profit).label('profit'),
        func.count(Sale.id).label('count')
    ).filter(
        and_(Sale.user_id == current_user.id, Sale.created_at >= today_start)
    ).first()

    # Dünkü satışlar
    yesterday_sales = db.query(
        func.sum(Sale.total_price).label('revenue')
    ).filter(
        and_(
            Sale.user_id == current_user.id,
            Sale.created_at >= yesterday_start,
            Sale.created_at < today_start
        )
    ).first()

    today_revenue = today_sales.revenue or 0.0
    today_profit = today_sales.profit or 0.0
    today_count = today_sales.count or 0
    yesterday_revenue = yesterday_sales.revenue or 0.0

    change = ((today_revenue - yesterday_revenue) / yesterday_revenue * 100) if yesterday_revenue > 0 else 0.0

    return {
        "today_sales": round(today_revenue, 2),
        "today_profit": round(today_profit, 2),
        "today_transactions": today_count,
        "sales_change": round(change, 1)
    }


@app.get("/dashboard/low_stock")
def get_low_stock(
    threshold: int = 10,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Az kalan ürünler (Sadece kendi ürünleri)"""
    products = db.query(Product).filter(
        and_(Product.user_id == current_user.id, Product.stock <= threshold)
    ).order_by(Product.stock).limit(10).all()

    return [
        {
            "id": p.id,
            "name": p.name,
            "stock": p.stock,
            "category": p.category
        }
        for p in products
    ]


@app.get("/dashboard/top_selling")
def get_top_selling(
    days: int = 1,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """En çok satanlar (Sadece kendi satışları)"""
    start_date = datetime.now() - timedelta(days=days)

    results = db.query(
        Product.name,
        func.sum(Sale.quantity).label('total_qty'),
        func.sum(Sale.total_price).label('total_revenue')
    ).join(Sale).filter(
        and_(Sale.user_id == current_user.id, Sale.created_at >= start_date)
    ).group_by(Product.id).order_by(func.sum(Sale.quantity).desc()).limit(10).all()

    return [
        {
            "name": r.name,
            "quantity": r.total_qty,
            "revenue": round(r.total_revenue, 2)
        }
        for r in results
    ]


# --- PRODUCTS (Multi-Tenant) ---

@app.get("/products")
def get_products(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Tüm ürünleri listele (Sadece kendi ürünleri)"""
    products = db.query(Product).filter(Product.user_id == current_user.id).all()
    return products


@app.post("/products")
def create_product(
    product: ProductCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Yeni ürün ekle (Kendi hesabına)"""
    db_product = Product(**product.dict(), user_id=current_user.id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.put("/products/{product_id}/stock")
def update_stock(
    product_id: int,
    stock: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Stok güncelle (Sadece kendi ürünü)"""
    product = db.query(Product).filter(
        and_(Product.id == product_id, Product.user_id == current_user.id)
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı veya yetkiniz yok")

    product.stock = stock
    db.commit()
    return {"message": "Stok güncellendi", "product": product}


# --- SALES (Multi-Tenant) ---

@app.post("/sales")
def create_sale(
    sale: SaleCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Yeni satış kaydet (Sadece kendi ürünü)"""
    product = db.query(Product).filter(
        and_(Product.id == sale.product_id, Product.user_id == current_user.id)
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı veya yetkiniz yok")

    if product.stock < sale.quantity:
        raise HTTPException(status_code=400, detail=f"Yetersiz stok! Mevcut: {product.stock}")

    total_price = product.sell_price * sale.quantity
    cost = product.cost_price * sale.quantity
    profit = total_price - cost

    db_sale = Sale(
        user_id=current_user.id,
        product_id=product.id,
        quantity=sale.quantity,
        unit_price=product.sell_price,
        total_price=total_price,
        cost=cost,
        profit=profit
    )
    db.add(db_sale)

    product.stock -= sale.quantity
    db.commit()
    db.refresh(db_sale)

    return {
        "message": "Satış kaydedildi!",
        "sale": db_sale,
        "remaining_stock": product.stock
    }


@app.get("/sales/recent")
def get_recent_sales(
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Son satışlar (Sadece kendi satışları)"""
    sales = db.query(Sale).filter(
        Sale.user_id == current_user.id
    ).order_by(Sale.created_at.desc()).limit(limit).all()

    result = []
    for sale in sales:
        product = db.query(Product).filter(Product.id == sale.product_id).first()
        result.append({
            "id": sale.id,
            "product_name": product.name if product else "Bilinmeyen",
            "quantity": sale.quantity,
            "total_price": sale.total_price,
            "profit": sale.profit,
            "created_at": sale.created_at.isoformat()
        })

    return result


# --- HEALTH CHECK ---

@app.get("/")
def root():
    """API sağlık kontrolü"""
    return {
        "status": "OK",
        "app": "BüfeOS",
        "version": "2.0.0 (Multi-Tenant)",
        "message": "Production-ready! 🚀"
    }
