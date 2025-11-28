"""
BüfeOS - Database Configuration
Basit SQLite database setup
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# SQLite database (offline çalışır!)
SQLALCHEMY_DATABASE_URL = "sqlite:///./bufeos.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# --- MODELS ---

class Product(Base):
    """Ürünler - Basitleştirilmiş, LOT tracking YOK"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    barcode = Column(String, unique=True, index=True)
    stock = Column(Integer, default=0)
    cost_price = Column(Float, default=0.0)  # Alış fiyatı
    sell_price = Column(Float, nullable=False)  # Satış fiyatı
    category = Column(String, default="Genel")
    image_url = Column(String, nullable=True)

    # İlişkiler
    sales = relationship("Sale", back_populates="product")
    alerts = relationship("StockAlert", back_populates="product")


class Sale(Base):
    """Satışlar - Her satış kaydı"""
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)  # Birim satış fiyatı
    total_price = Column(Float, nullable=False)  # Toplam fiyat
    cost = Column(Float, default=0.0)  # Toplam maliyet
    profit = Column(Float, default=0.0)  # Kar
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # İlişki
    product = relationship("Product", back_populates="sales")


class StockAlert(Base):
    """Stok Uyarıları - Basit threshold sistemi"""
    __tablename__ = "stock_alerts"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    alert_type = Column(String, nullable=False)  # 'low_stock' veya 'out_of_stock'
    threshold = Column(Integer, default=5)  # Minimum stok
    is_active = Column(Integer, default=1)  # 1=aktif, 0=pasif
    created_at = Column(DateTime, default=datetime.utcnow)

    # İlişki
    product = relationship("Product", back_populates="alerts")


# Database oluştur
def init_db():
    """Veritabanını başlat"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created!")


# Dependency
def get_db():
    """FastAPI dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
