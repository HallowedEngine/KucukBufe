"""
BüfeOS - Database Configuration (Multi-Tenant Production)
PostgreSQL için hazır - Her büfe ayrı data
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Production: PostgreSQL (Railway/Render)
# Local: SQLite
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./bufeos.db"
)

# PostgreSQL URL düzeltmesi (Railway/Heroku eski format kullanır)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# --- MODELS ---

class User(Base):
    """Büfe Sahipleri - Multi-tenant"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Büfe Bilgileri
    bufe_adi = Column(String, nullable=False)
    telefon = Column(String)
    adres = Column(String)

    # Abonelik
    is_active = Column(Boolean, default=True)
    is_trial = Column(Boolean, default=True)
    trial_ends_at = Column(DateTime)
    subscription_type = Column(String, default="trial")

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

    # İlişkiler
    products = relationship("Product", back_populates="owner", cascade="all, delete-orphan")
    sales = relationship("Sale", back_populates="owner", cascade="all, delete-orphan")


class Product(Base):
    """Ürünler - Her büfe kendi ürünleri"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # ✨ Multi-tenant

    name = Column(String, nullable=False, index=True)
    barcode = Column(String, index=True)  # Artık unique değil (her büfenin aynı barkodu olabilir)
    stock = Column(Integer, default=0)
    cost_price = Column(Float, default=0.0)
    sell_price = Column(Float, nullable=False)
    category = Column(String, default="Genel")
    image_url = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # İlişkiler
    owner = relationship("User", back_populates="products")
    sales = relationship("Sale", back_populates="product")
    alerts = relationship("StockAlert", back_populates="product")


class Sale(Base):
    """Satışlar - Her büfe kendi satışları"""
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # ✨ Multi-tenant
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    cost = Column(Float, default=0.0)
    profit = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # İlişkiler
    owner = relationship("User", back_populates="sales")
    product = relationship("Product", back_populates="sales")


class StockAlert(Base):
    """Stok Uyarıları"""
    __tablename__ = "stock_alerts"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    alert_type = Column(String, nullable=False)
    threshold = Column(Integer, default=5)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    # İlişki
    product = relationship("Product", back_populates="alerts")


# Database oluştur
def init_db():
    """Veritabanını başlat"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created (Multi-tenant)!")


# Dependency
def get_db():
    """FastAPI dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
