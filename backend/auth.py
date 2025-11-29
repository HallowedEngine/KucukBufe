"""
BüfeOS - User Authentication & Multi-Tenant
Production-ready authentication system
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import hashlib
import secrets

from database import Base

security = HTTPBasic()


# --- MODELS ---

class User(Base):
    """Büfe Kullanıcıları - Multi-tenant için"""
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
    is_trial = Column(Boolean, default=True)  # İlk ay ücretsiz
    trial_ends_at = Column(DateTime)  # Trial bitiş tarihi
    subscription_type = Column(String, default="trial")  # trial, monthly, yearly

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

    # İlişkiler - Her kullanıcının kendi ürünleri/satışları
    products = relationship("Product", back_populates="owner")
    sales = relationship("Sale", back_populates="owner")


# --- PASSWORD HASHING ---

def hash_password(password: str) -> str:
    """Şifreyi güvenli şekilde hashle"""
    salt = "bufeos_secret_salt_2024"  # Production'da env variable kullan!
    return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Şifre doğrulama"""
    return hash_password(plain_password) == hashed_password


# --- AUTHENTICATION ---

def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security),
    db = Depends(get_db)
) -> User:
    """Mevcut kullanıcıyı al (Basic Auth ile)"""

    # Email veya username ile giriş
    user = db.query(User).filter(
        (User.email == credentials.username) |
        (User.username == credentials.username)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kullanıcı bulunamadı",
            headers={"WWW-Authenticate": "Basic"},
        )

    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Şifre hatalı",
            headers={"WWW-Authenticate": "Basic"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hesabınız askıya alınmış. Lütfen destek ile iletişime geçin."
        )

    # Son giriş zamanını güncelle
    user.last_login = datetime.utcnow()
    db.commit()

    return user


# --- AUTHORIZATION ---

def check_subscription(user: User):
    """Abonelik kontrolü"""
    if user.is_trial:
        # Trial süresi dolmuş mu?
        if user.trial_ends_at and datetime.utcnow() > user.trial_ends_at:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Ücretsiz deneme süreniz doldu. Lütfen aboneliğinizi yükseltin."
            )

    return True


# --- DEPENDENCY ---
from database import get_db

def get_current_active_user(
    user: User = Depends(get_current_user)
) -> User:
    """Aktif ve aboneliği geçerli kullanıcı"""
    check_subscription(user)
    return user
