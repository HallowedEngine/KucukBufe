"""
BüfeOS - Demo Veri Yükleyici
Tipik büfe ürünleri ve örnek satışlar
"""
from sqlalchemy.orm import Session
from database import SessionLocal, Product, Sale, init_db
from datetime import datetime, timedelta
import random

def load_demo_products():
    """Tipik büfe ürünlerini yükle"""
    db = SessionLocal()

    # Ekmek & Unlu Mamüller
    products = [
        # Ekmek & Unlu Mamüller
        {"name": "Simit", "barcode": "8690001001", "stock": 25, "cost_price": 3.0, "sell_price": 5.0, "category": "Ekmek"},
        {"name": "Poğaça", "barcode": "8690001002", "stock": 15, "cost_price": 4.0, "sell_price": 7.0, "category": "Ekmek"},
        {"name": "Sandviç", "barcode": "8690001003", "stock": 10, "cost_price": 12.0, "sell_price": 20.0, "category": "Ekmek"},
        {"name": "Açma", "barcode": "8690001004", "stock": 12, "cost_price": 3.5, "sell_price": 6.0, "category": "Ekmek"},

        # İçecekler - Su
        {"name": "Su 0.5L", "barcode": "8690002001", "stock": 48, "cost_price": 1.5, "sell_price": 3.0, "category": "İçecek"},
        {"name": "Su 1.5L", "barcode": "8690002002", "stock": 24, "cost_price": 3.0, "sell_price": 5.0, "category": "İçecek"},
        {"name": "Soda 200ml", "barcode": "8690002003", "stock": 36, "cost_price": 2.5, "sell_price": 5.0, "category": "İçecek"},

        # İçecekler - Gazlı
        {"name": "Coca Cola 330ml", "barcode": "8690002010", "stock": 36, "cost_price": 6.0, "sell_price": 10.0, "category": "İçecek"},
        {"name": "Fanta 330ml", "barcode": "8690002011", "stock": 24, "cost_price": 6.0, "sell_price": 10.0, "category": "İçecek"},
        {"name": "Sprite 330ml", "barcode": "8690002012", "stock": 24, "cost_price": 6.0, "sell_price": 10.0, "category": "İçecek"},

        # İçecekler - Süt Ürünleri
        {"name": "Ayran 250ml", "barcode": "8690002020", "stock": 30, "cost_price": 3.5, "sell_price": 6.0, "category": "İçecek"},
        {"name": "Süt 200ml", "barcode": "8690002021", "stock": 18, "cost_price": 4.0, "sell_price": 7.0, "category": "İçecek"},

        # İçecekler - Meyve Suyu
        {"name": "Ice Tea Şeftali 330ml", "barcode": "8690002030", "stock": 24, "cost_price": 5.0, "sell_price": 8.0, "category": "İçecek"},
        {"name": "Cappy Portakal 200ml", "barcode": "8690002031", "stock": 24, "cost_price": 4.5, "sell_price": 7.0, "category": "İçecek"},

        # Sigaralar (En önemli kategori!)
        {"name": "Marlboro Touch", "barcode": "8690003001", "stock": 8, "cost_price": 48.0, "sell_price": 55.0, "category": "Sigara"},
        {"name": "Winston Blue", "barcode": "8690003002", "stock": 6, "cost_price": 45.0, "sell_price": 52.0, "category": "Sigara"},
        {"name": "Parliament Night Blue", "barcode": "8690003003", "stock": 5, "cost_price": 50.0, "sell_price": 57.0, "category": "Sigara"},
        {"name": "Camel Blue", "barcode": "8690003004", "stock": 7, "cost_price": 46.0, "sell_price": 53.0, "category": "Sigara"},
        {"name": "L&M Blue", "barcode": "8690003005", "stock": 10, "cost_price": 42.0, "sell_price": 49.0, "category": "Sigara"},

        # Atıştırmalıklar - Çikolata
        {"name": "Ülker Çikolata 60g", "barcode": "8690004001", "stock": 20, "cost_price": 8.0, "sell_price": 12.0, "category": "Atıştırmalık"},
        {"name": "Eti Karam Gurme", "barcode": "8690004002", "stock": 15, "cost_price": 6.0, "sell_price": 10.0, "category": "Atıştırmalık"},
        {"name": "Snickers", "barcode": "8690004003", "stock": 12, "cost_price": 7.0, "sell_price": 11.0, "category": "Atıştırmalık"},

        # Atıştırmalıklar - Cips
        {"name": "Lays Klasik 96g", "barcode": "8690004010", "stock": 18, "cost_price": 12.0, "sell_price": 18.0, "category": "Atıştırmalık"},
        {"name": "Doritos Nacho 113g", "barcode": "8690004011", "stock": 15, "cost_price": 14.0, "sell_price": 20.0, "category": "Atıştırmalık"},
        {"name": "Ruffles 107g", "barcode": "8690004012", "stock": 12, "cost_price": 13.0, "sell_price": 19.0, "category": "Atıştırmalık"},

        # Atıştırmalıklar - Kuruyemiş
        {"name": "Fındık 100g", "barcode": "8690004020", "stock": 10, "cost_price": 25.0, "sell_price": 35.0, "category": "Atıştırmalık"},
        {"name": "Fıstık 100g", "barcode": "8690004021", "stock": 8, "cost_price": 30.0, "sell_price": 40.0, "category": "Atıştırmalık"},
        {"name": "Çekirdek 150g", "barcode": "8690004022", "stock": 15, "cost_price": 8.0, "sell_price": 12.0, "category": "Atıştırmalık"},

        # Sıcak İçecekler
        {"name": "Çay", "barcode": None, "stock": 100, "cost_price": 1.0, "sell_price": 3.0, "category": "Sıcak İçecek"},
        {"name": "Türk Kahvesi", "barcode": None, "stock": 50, "cost_price": 5.0, "sell_price": 10.0, "category": "Sıcak İçecek"},
        {"name": "Nescafe", "barcode": None, "stock": 60, "cost_price": 3.0, "sell_price": 7.0, "category": "Sıcak İçecek"},

        # Diğer
        {"name": "Sakız Falim", "barcode": "8690005001", "stock": 40, "cost_price": 1.5, "sell_price": 3.0, "category": "Diğer"},
        {"name": "Şeker (adet)", "barcode": "8690005002", "stock": 100, "cost_price": 0.5, "sell_price": 1.0, "category": "Diğer"},
        {"name": "Naneli (adet)", "barcode": "8690005003", "stock": 80, "cost_price": 0.5, "sell_price": 1.0, "category": "Diğer"},
    ]

    for p_data in products:
        product = Product(**p_data)
        db.add(product)

    db.commit()
    print(f"✅ {len(products)} adet ürün eklendi!")
    db.close()


def generate_demo_sales():
    """Son 7 günlük örnek satışlar oluştur"""
    db = SessionLocal()

    products = db.query(Product).all()
    if not products:
        print("⚠️  Önce ürün ekleyin!")
        return

    # Son 7 gün için satış oluştur
    for days_ago in range(7):
        sale_date = datetime.now() - timedelta(days=days_ago)

        # Günde 30-80 arası satış
        num_sales = random.randint(30, 80)

        for _ in range(num_sales):
            # Rastgele ürün seç (sık satılanları daha çok seç)
            # Çay, su, simit, sigara daha sık satılır
            product = random.choice(products)

            # Kategori bazlı satış olasılığı
            if product.category in ["Sigara", "İçecek", "Ekmek", "Sıcak İçecek"]:
                if random.random() > 0.3:  # %70 şans
                    quantity = random.randint(1, 3)
                else:
                    continue
            else:
                if random.random() > 0.6:  # %40 şans
                    quantity = 1
                else:
                    continue

            # Satış zamanını rastgele ayarla (07:00 - 22:00 arası)
            hour = random.randint(7, 22)
            minute = random.randint(0, 59)
            sale_time = sale_date.replace(hour=hour, minute=minute, second=0)

            total_price = product.sell_price * quantity
            cost = product.cost_price * quantity
            profit = total_price - cost

            sale = Sale(
                product_id=product.id,
                quantity=quantity,
                unit_price=product.sell_price,
                total_price=total_price,
                cost=cost,
                profit=profit,
                created_at=sale_time
            )
            db.add(sale)

    db.commit()
    print(f"✅ 7 günlük demo satış verisi oluşturuldu!")
    db.close()


if __name__ == "__main__":
    print("🚀 BüfeOS Demo Veri Yükleniyor...")

    # DB başlat
    init_db()

    # Ürünleri yükle
    load_demo_products()

    # Demo satışlar
    generate_demo_sales()

    print("✅ Demo veri yükleme tamamlandı!")
