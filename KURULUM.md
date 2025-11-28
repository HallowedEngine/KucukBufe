# 🚀 BüfeOS Kurulum Rehberi

## Windows Kullanıcıları İçin

### 1. Python Kurulumu

1. [Python İndir](https://www.python.org/downloads/) - **Python 3.8 veya üzeri**
2. Kurulum sırasında **"Add Python to PATH"** seçeneğini işaretleyin
3. Kurulumu tamamlayın

### 2. BüfeOS Kurulumu

1. BüfeOS klasörünü bilgisayarınıza indirin
2. `BUFE_BASLAT.bat` dosyasına çift tıklayın
3. İlk açılışta gerekli bağımlılıklar otomatik yüklenecektir
4. Demo veriler otomatik oluşturulacaktır

### 3. Kullanım

- **Başlatma**: `BUFE_BASLAT.bat`
- **Tarayıcıda Açma**: http://localhost:8000/templates/index.html
- **Durdurma**: Komut penceresinde `Ctrl+C`

---

## Linux/Mac Kullanıcıları İçin

### 1. Python Kontrolü

```bash
# Python sürümünü kontrol edin
python3 --version

# Python yoksa yükleyin
sudo apt install python3 python3-pip  # Ubuntu/Debian
# veya
brew install python3  # Mac
```

### 2. BüfeOS Kurulumu

```bash
# Klasöre girin
cd KucukBufe

# Bağımlılıkları yükleyin
pip3 install -r requirements.txt

# Demo veri yükleyin (opsiyonel)
cd backend
python3 demo_data.py
cd ..
```

### 3. Çalıştırma

```bash
# Sunucuyu başlatın
./start.sh

# Tarayıcıda açın
http://localhost:8000/templates/index.html
```

---

## 🎯 İlk Kullanım

### Adım 1: Demo Verilerle Başlayın

İlk açılışta sistem otomatik olarak demo veriler oluşturur:
- 34 tipik büfe ürünü (simit, su, sigara, vb.)
- 7 günlük satış geçmişi

### Adım 2: Ana Paneli Keşfedin

1. **Bugünkü Satış**: Günlük ciro ve kar
2. **Stok Uyarıları**: Az kalan ürünler
3. **En Çok Satanlar**: Popüler ürünler

### Adım 3: İlk Satışınızı Yapın

1. **Hızlı Satış** sayfasına gidin
2. Ürün seçin veya barkod okutun
3. **Satışı Tamamla** butonuna basın

### Adım 4: Kendi Ürünlerinizi Ekleyin

#### CSV ile (Önerilen)

1. Excel'de şu formatta dosya oluşturun:

```
urun_adi,barkod,stok,satis_fiyat,alis_fiyat,kategori
Simit,8690123456,50,5.0,3.0,Ekmek
```

2. **Ürünler** sayfasında **CSV Yükle** butonuna tıklayın
3. Dosyanızı seçin ve yükleyin

#### Manuel Ekleme

1. **Ürünler** sayfasında **Yeni Ürün Ekle**
2. Formu doldurun
3. **Ürün Ekle** butonuna basın

---

## 📱 Mobil Kullanım

BüfeOS mobil cihazlarda da çalışır!

### Seçenek 1: Tarayıcı (Basit)

1. Bilgisayarınızın IP adresini öğrenin:
   - Windows: `ipconfig`
   - Linux/Mac: `ifconfig`

2. Mobil tarayıcıda açın:
   ```
   http://[BILGISAYAR_IP]:8000/templates/index.html
   ```
   Örnek: http://192.168.1.100:8000/templates/index.html

### Seçenek 2: Ana Ekrana Ekle (İleri)

1. Chrome/Safari'de siteyi açın
2. **Menü** → **Ana ekrana ekle**
3. Artık bir uygulama gibi açılacak!

---

## 💾 Yedekleme

### Manuel Yedekleme

```bash
# Database dosyasını kopyalayın
cp backend/bufeos.db backup/bufeos_$(date +%Y%m%d).db
```

### Windows için Otomatik Yedekleme

`YEDEKLE.bat` oluşturun:

```batch
@echo off
copy backend\bufeos.db backup\bufeos_%date:~-4,4%%date:~-7,2%%date:~-10,2%.db
echo Yedekleme tamamlandı!
pause
```

---

## 🔧 Sorun Giderme

### "Port 8000 kullanımda" Hatası

```bash
# Çalışan süreci bulun ve durdurun
lsof -ti:8000 | xargs kill -9  # Linux/Mac
netstat -ano | findstr :8000   # Windows
```

### "Module not found" Hatası

```bash
# Bağımlılıkları yeniden yükleyin
pip install -r requirements.txt
```

### Database Sıfırlama

```bash
# Database'i silin (YEDEKLEYİN ÖNCE!)
rm backend/bufeos.db

# Sunucuyu başlatın, yeni database oluşturulacak
./start.sh

# Demo veri yükleyin
cd backend && python demo_data.py
```

### Frontend Görünmüyor

Tarayıcınızda doğru URL'i açtığınızdan emin olun:
```
http://localhost:8000/templates/index.html
```

NOT: `http://localhost:8000` değil!

---

## 🎓 Video Eğitimler (Gelecek)

- [ ] BüfeOS'a İlk Adım (5 dk)
- [ ] İlk Ürünlerinizi Ekleme (3 dk)
- [ ] Hızlı Satış Yapma (2 dk)
- [ ] Sipariş Listesi Oluşturma (4 dk)

---

## 📞 Yardıma İhtiyacınız mı Var?

1. **GitHub Issues**: Sorun bildirin
2. **README.md**: Detaylı dokümantasyon
3. **Discord** (yakında): Topluluk desteği

---

**BüfeOS ile kolay gelsin! 🏪**
