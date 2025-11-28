# 🏪 BüfeOS - Küçük Büfe Stok Yönetim Sistemi

**BüfeOS**, küçük büfeler ve bakkallar için tasarlanmış basit, hızlı ve **offline çalışabilen** bir stok yönetim sistemidir.

## ✨ Özellikler

### 📊 Ana Dashboard
- **Bugünkü Satış Özeti**: Günlük ciro, kar ve işlem sayısı
- **Stok Uyarıları**: Az kalan veya biten ürünler
- **En Çok Satanlar**: Günlük popüler ürünler
- **Son Satışlar**: Gerçek zamanlı satış takibi

### 💰 Hızlı Satış Girişi
- Barkod okuyucu desteği
- Kategori bazlı hızlı ürün seçimi
- Mobil-friendly büyük butonlar
- Sepet yönetimi
- Anlık stok güncelleme

### 📦 Ürün Yönetimi
- CSV ile toplu ürün yükleme
- Hızlı stok güncelleme
- Kategori yönetimi
- Kar marjı hesaplama

### 📋 Akıllı Sipariş Listesi
- Otomatik sipariş önerisi (son 7 günlük satış verisine göre)
- WhatsApp entegrasyonu
- Kategori bazlı gruplama

---

## 🚀 Hızlı Başlangıç

### Gereksinimler
- Python 3.8+
- Web tarayıcı (Chrome, Firefox, Safari)

### 1. Kurulum

```bash
# Depoyu klonlayın
git clone <repository-url>
cd KucukBufe

# Python bağımlılıklarını yükleyin
pip install -r requirements.txt
```

### 2. Demo Veriyi Yükleyin (İsteğe Bağlı)

```bash
cd backend
python demo_data.py
```

Bu komut:
- Tipik büfe ürünlerini ekler (simit, su, sigara, vb.)
- Son 7 günlük demo satışlar oluşturur

### 3. Sunucuyu Başlatın

#### Linux/Mac:
```bash
chmod +x start.sh
./start.sh
```

#### Windows:
```bash
BUFE_BASLAT.bat
```

### 4. Tarayıcıda Açın

Tarayıcınızda şu adresi açın:
```
http://localhost:8000/templates/index.html
```

---

## 📁 Proje Yapısı

```
KucukBufe/
├── backend/
│   ├── main.py           # FastAPI uygulaması
│   ├── database.py       # SQLAlchemy modeller
│   └── demo_data.py      # Demo veri yükleyici
├── templates/
│   ├── index.html        # Ana dashboard
│   ├── sales.html        # Hızlı satış sayfası
│   ├── products.html     # Ürün yönetimi
│   └── orders.html       # Sipariş listesi
├── bufeos.db             # SQLite veritabanı (otomatik oluşur)
├── requirements.txt      # Python bağımlılıkları
└── README.md
```

---

## 🛠️ API Endpoints

### Dashboard
- `GET /dashboard/sales_today` - Bugünkü satış özeti
- `GET /dashboard/low_stock?threshold=10` - Az kalan ürünler
- `GET /dashboard/top_selling?days=1` - En çok satanlar

### Products
- `GET /products` - Tüm ürünleri listele
- `POST /products` - Yeni ürün ekle
- `PUT /products/{id}/stock?stock=X` - Stok güncelle
- `POST /products/upload_csv` - CSV ile ürün yükle

### Sales
- `POST /sales` - Yeni satış kaydet
- `GET /sales/recent?limit=20` - Son satışları getir

### Orders
- `GET /orders/suggest?threshold=10` - Sipariş önerisi

---

## 📊 CSV Ürün Yükleme Formatı

```csv
urun_adi,barkod,stok,satis_fiyat,alis_fiyat,kategori
Simit,8690123456,50,5.0,3.0,Ekmek
Su 0.5L,8690123457,100,3.0,1.5,İçecek
Marlboro,8690123458,20,55.0,48.0,Sigara
```

**Önemli Notlar:**
- İlk satır başlık satırıdır (atlayın veya olduğu gibi bırakın)
- Barkod boş olabilir
- Kategori: Ekmek, İçecek, Sigara, Atıştırmalık, Sıcak İçecek, Diğer

---

## 🎯 Hedef Kullanıcı

- **Büfe Sahipleri**: 50-100 çeşit ürün satan küçük işletmeler
- **Bakkallar**: Mahalle bakkalları
- **Kantinler**: Okul, işyeri kantinleri

### Çözülen Sorunlar

| Sorun | BüfeOS Çözümü |
|-------|---------------|
| ❌ Manuel defter tutma | ✅ Otomatik satış kaydı |
| ❌ Hangi ürün karlı bilmiyorum | ✅ Kar marjı analizi |
| ❌ Stok kontrolü zor | ✅ Otomatik stok uyarıları |
| ❌ Neyin bittiğini anlamıyorum | ✅ Akıllı sipariş önerisi |
| ❌ Pahalı ERP sistemleri | ✅ Ücretsiz, basit çözüm |

---

## 💰 Fiyatlandırma (Gelecek Plan)

- **Beta Kullanıcılar**: Ücretsiz (İlk 10 kullanıcı)
- **Aylık**: 99 TL/ay
- **Yıllık**: 990 TL/yıl (2 ay bedava)

---

## 🔒 Offline Kullanım

BüfeOS **tamamen offline çalışır**:
- Veritabanı: SQLite (lokal dosya)
- Sunucu: Localhost (internetе gerek yok)
- Yedekleme: `bufeos.db` dosyasını kopyalayın

### Yedekleme Nasıl Yapılır?

```bash
# Windows
copy bufeos.db bufeos_backup_2024_11_28.db

# Linux/Mac
cp bufeos.db bufeos_backup_$(date +%Y_%m_%d).db
```

---

## 🛡️ Güvenlik

- Veriler sadece sizin bilgisayarınızda saklanır
- İnternet bağlantısı gerektirmez
- Üçüncü taraf veri paylaşımı YOK

---

## 🤝 Katkıda Bulunma

Bu bir **pivot projesidir**. Geri bildirimleriniz çok değerli!

Önerileriniz için:
- Issue açın
- Pull request gönderin
- Bize ulaşın: [email korunuyor]

---

## 📞 Destek

Sorun mu yaşıyorsunuz?
1. GitHub Issues'dan sorun açın
2. Demo veriyi yeniden yükleyin: `python backend/demo_data.py`
3. Veritabanını sıfırlayın: `bufeos.db` dosyasını silin ve sunucuyu yeniden başlatın

---

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

---

## 🎓 Pivot Hikayesi

**Neden BüfeOS?**

1. **Başlangıç**: Orta ölçekli marketler için stok sistemi geliştirdik
2. **Geri Bildirim**: "Çeşitlilik az, bizim için yeterli değil" ❌
3. **Analiz**: Marketler binlerce ürün takip ediyor, bizim sistem 50-200 ürün için ideal
4. **Pivot**: Küçük büfelere odaklandık! ✅

**Neden Büfe Daha İyi?**
- ✅ 50-100 ürün (sistemimiz için ideal)
- ✅ Hiç sistemi yok (büyük ihtiyaç)
- ✅ Sahibi = işletmeci (hızlı karar)
- ✅ Manuel çalışıyor (otomasyon değer katar)

---

## 🚀 Yol Haritası

### ✅ MVP (Tamamlandı)
- 3 kartlı basit dashboard
- Hızlı satış girişi
- Ürün yönetimi
- Sipariş listesi

### 🔜 Gelecek Özellikler
- [ ] PWA (Progressive Web App) - Telefona yüklenebilir
- [ ] PDF raporlar (günlük/haftalık/aylık)
- [ ] Çoklu kullanıcı desteği
- [ ] Cloud backup (isteğe bağlı)
- [ ] Mobil uygulama (Android/iOS)

---

**BüfeOS ile büfenizi kolayca yönetin! 🏪**
