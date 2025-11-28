"""
BüfeOS - Ana API
Basit, hızlı, offline büfe yönetim sistemi
"""
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
import csv
import io
from typing import List, Optional
from pydantic import BaseModel

from database import get_db, init_db, Product, Sale, StockAlert

# FastAPI app
app = FastAPI(
    title="BüfeOS API",
    description="Küçük büfeler için basit stok yönetim sistemi",
    version="1.0.0"
)

# CORS (frontend için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (parent directory)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
app.mount("/templates", StaticFiles(directory=os.path.join(BASE_DIR, "templates"), html=True), name="templates")


# --- PYDANTIC MODELS ---

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


class DashboardResponse(BaseModel):
    today_sales: float
    today_profit: float
    today_transactions: int
    sales_change: float  # Dünle karşılaştırma


class LowStockItem(BaseModel):
    id: int
    name: str
    stock: int
    category: str


class TopSellingItem(BaseModel):
    name: str
    quantity: int
    revenue: float


# --- STARTUP ---

@app.on_event("startup")
def startup():
    """Uygulama başlarken DB'yi başlat"""
    init_db()
    print("🚀 BüfeOS başlatıldı!")


# --- DASHBOARD ENDPOINTS ---

@app.get("/dashboard/sales_today", response_model=DashboardResponse)
def get_sales_today(db: Session = Depends(get_db)):
    """Bugünkü satış özeti"""
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = today_start - timedelta(days=1)

    # Bugünkü satışlar
    today_sales = db.query(
        func.sum(Sale.total_price).label('revenue'),
        func.sum(Sale.profit).label('profit'),
        func.count(Sale.id).label('count')
    ).filter(Sale.created_at >= today_start).first()

    # Dünkü satışlar (karşılaştırma için)
    yesterday_sales = db.query(
        func.sum(Sale.total_price).label('revenue')
    ).filter(
        and_(Sale.created_at >= yesterday_start, Sale.created_at < today_start)
    ).first()

    today_revenue = today_sales.revenue or 0.0
    today_profit = today_sales.profit or 0.0
    today_count = today_sales.count or 0
    yesterday_revenue = yesterday_sales.revenue or 0.0

    # Değişim yüzdesi
    if yesterday_revenue > 0:
        change = ((today_revenue - yesterday_revenue) / yesterday_revenue) * 100
    else:
        change = 0.0

    return {
        "today_sales": round(today_revenue, 2),
        "today_profit": round(today_profit, 2),
        "today_transactions": today_count,
        "sales_change": round(change, 1)
    }


@app.get("/dashboard/low_stock", response_model=List[LowStockItem])
def get_low_stock(threshold: int = 10, db: Session = Depends(get_db)):
    """Az kalan ürünler"""
    products = db.query(Product).filter(Product.stock <= threshold).order_by(Product.stock).limit(10).all()

    return [
        {
            "id": p.id,
            "name": p.name,
            "stock": p.stock,
            "category": p.category
        }
        for p in products
    ]


@app.get("/dashboard/top_selling", response_model=List[TopSellingItem])
def get_top_selling(days: int = 1, db: Session = Depends(get_db)):
    """En çok satanlar (varsayılan: bugün)"""
    start_date = datetime.now() - timedelta(days=days)

    results = db.query(
        Product.name,
        func.sum(Sale.quantity).label('total_qty'),
        func.sum(Sale.total_price).label('total_revenue')
    ).join(Sale).filter(
        Sale.created_at >= start_date
    ).group_by(Product.id).order_by(func.sum(Sale.quantity).desc()).limit(10).all()

    return [
        {
            "name": r.name,
            "quantity": r.total_qty,
            "revenue": round(r.total_revenue, 2)
        }
        for r in results
    ]


# --- PRODUCTS ---

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    """Tüm ürünleri listele"""
    products = db.query(Product).all()
    return products


@app.post("/products")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Yeni ürün ekle"""
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.put("/products/{product_id}/stock")
def update_stock(product_id: int, stock: int, db: Session = Depends(get_db)):
    """Stok güncelle"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")

    product.stock = stock
    db.commit()
    return {"message": "Stok güncellendi", "product": product}


# --- SALES ---

@app.post("/sales")
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    """Yeni satış kaydet"""
    # Ürünü bul
    product = db.query(Product).filter(Product.id == sale.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")

    # Stok kontrolü
    if product.stock < sale.quantity:
        raise HTTPException(status_code=400, detail=f"Yetersiz stok! Mevcut: {product.stock}")

    # Satış hesapla
    total_price = product.sell_price * sale.quantity
    cost = product.cost_price * sale.quantity
    profit = total_price - cost

    # Satış kaydı oluştur
    db_sale = Sale(
        product_id=product.id,
        quantity=sale.quantity,
        unit_price=product.sell_price,
        total_price=total_price,
        cost=cost,
        profit=profit
    )
    db.add(db_sale)

    # Stok azalt
    product.stock -= sale.quantity

    db.commit()
    db.refresh(db_sale)

    return {
        "message": "Satış kaydedildi!",
        "sale": db_sale,
        "remaining_stock": product.stock
    }


@app.get("/sales/recent")
def get_recent_sales(limit: int = 20, db: Session = Depends(get_db)):
    """Son satışlar"""
    sales = db.query(Sale).order_by(Sale.created_at.desc()).limit(limit).all()

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


# --- CSV UPLOAD ---

@app.post("/products/upload_csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    CSV ile toplu ürün yükleme
    Format: urun_adi,barkod,stok,satis_fiyat,alis_fiyat,kategori
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Sadece CSV dosyası yükleyebilirsiniz")

    contents = await file.read()
    decoded = contents.decode('utf-8-sig')  # BOM karakterini kaldır

    csv_reader = csv.DictReader(io.StringIO(decoded))

    added = 0
    updated = 0
    errors = []

    for row in csv_reader:
        try:
            name = row.get('urun_adi', '').strip()
            barcode = row.get('barkod', '').strip() or None
            stock = int(row.get('stok', 0))
            sell_price = float(row.get('satis_fiyat', 0))
            cost_price = float(row.get('alis_fiyat', 0))
            category = row.get('kategori', 'Genel').strip()

            # Barkod varsa kontrol et
            if barcode:
                existing = db.query(Product).filter(Product.barcode == barcode).first()
                if existing:
                    # Güncelle
                    existing.stock += stock
                    updated += 1
                else:
                    # Yeni ekle
                    product = Product(
                        name=name,
                        barcode=barcode,
                        stock=stock,
                        cost_price=cost_price,
                        sell_price=sell_price,
                        category=category
                    )
                    db.add(product)
                    added += 1
            else:
                # Barkod yoksa direkt ekle
                product = Product(
                    name=name,
                    barcode=None,
                    stock=stock,
                    cost_price=cost_price,
                    sell_price=sell_price,
                    category=category
                )
                db.add(product)
                added += 1

        except Exception as e:
            errors.append(f"{name}: {str(e)}")

    db.commit()

    return {
        "message": "CSV yükleme tamamlandı",
        "added": added,
        "updated": updated,
        "errors": errors
    }


# --- ORDER LIST ---

@app.get("/orders/suggest")
def suggest_order_list(threshold: int = 10, db: Session = Depends(get_db)):
    """Sipariş listesi öner (az kalan/biten ürünler)"""
    low_stock = db.query(Product).filter(Product.stock <= threshold).order_by(Product.stock).all()

    order_list = []
    for product in low_stock:
        # Haftalık ortalama satış
        week_ago = datetime.now() - timedelta(days=7)
        weekly_sales = db.query(func.sum(Sale.quantity)).filter(
            and_(Sale.product_id == product.id, Sale.created_at >= week_ago)
        ).scalar() or 0

        daily_avg = weekly_sales / 7
        suggested_qty = max(int(daily_avg * 7), 10)  # 1 haftalık + minimum 10

        order_list.append({
            "product_name": product.name,
            "current_stock": product.stock,
            "suggested_quantity": suggested_qty,
            "category": product.category
        })

    return order_list


# --- HEALTH CHECK ---

@app.get("/")
def root():
    """API sağlık kontrolü"""
    return {
        "status": "OK",
        "app": "BüfeOS",
        "version": "1.0.0",
        "message": "Küçük büfeler için stok yönetim sistemi 🏪"
    }
