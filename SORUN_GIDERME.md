# 🔧 Sorun Giderme Rehberi

## ❌ Yaygın Hatalar ve Çözümleri

### 1. "UNIQUE constraint failed: products.barcode"

**Neden Oluyor?**
- Demo veri zaten yüklenmiş, tekrar yüklemeye çalışıyor
- Barkodlar unique olduğu için hata veriyor

**Çözüm 1: Database'i Temizle (Önerilen)**

```batch
REM Windows
cd C:\Users\benyu\Desktop\KucukBufe\backend
del bufeos.db
cd ..
BUFE_BASLAT.bat
```

```bash
# Linux/Mac
cd ~/KucukBufe/backend
rm bufeos.db
cd ..
./start.sh
```

**Çözüm 2: Demo Veriyi Manuel Yükle**

```batch
REM Windows
cd backend
python demo_data.py
```

Eğer "Zaten X ürün var" mesajı alırsanız, veri zaten yüklenmiş demektir.

---

### 2. "RuntimeError: Directory does not exist"

**Neden Oluyor?**
- `static/` veya `frontend/` klasörleri eksik
- Git boş klasörleri klonlarken atlamış

**Çözüm: Klasörleri Manuel Oluştur**

```batch
REM Windows
cd C:\Users\benyu\Desktop\KucukBufe
mkdir static
mkdir frontend
BUFE_BASLAT.bat
```

```bash
# Linux/Mac
cd ~/KucukBufe
mkdir -p static frontend
./start.sh
```

**Kalıcı Çözüm:**

En son kodu çekin (düzeltme commit'i eklendi):

```bash
git pull origin claude/retail-inventory-system-01Mg1QmBSm836pepM7N2Crh6
```

---

### 3. "Port 8000 already in use"

**Neden Oluyor?**
- Başka bir BüfeOS süreci zaten çalışıyor
- Veya başka bir program 8000 portunu kullanıyor

**Çözüm:**

**Windows:**
```batch
REM Çalışan süreci bul
netstat -ano | findstr :8000

REM Process ID'yi (PID) al ve durdur
taskkill /PID [PID_BURAYA] /F
```

**Linux/Mac:**
```bash
# Çalışan süreci bul ve durdur
lsof -ti:8000 | xargs kill -9
```

---

### 4. "Module not found"

**Neden Oluyor?**
- Python bağımlılıkları yüklenmemiş

**Çözüm:**

```batch
REM Windows
cd C:\Users\benyu\Desktop\KucukBufe
pip install -r requirements.txt
```

```bash
# Linux/Mac
cd ~/KucukBufe
pip3 install -r requirements.txt
```

---

### 5. "Page Not Found (404)" - Frontend Açılmıyor

**Neden Oluyor?**
- Yanlış URL kullanıyorsunuz

**Doğru URL:**
```
http://localhost:8000/templates/index.html
```

**Yanlış URL'ler:**
- ❌ http://localhost:8000
- ❌ http://localhost:8000/index.html
- ❌ http://localhost:8000/templates

---

## 🔄 Tam Temizlik (Reset to Factory)

Herşeyi sıfırlayıp baştan başlamak isterseniz:

```batch
REM Windows
cd C:\Users\benyu\Desktop\KucukBufe
del backend\bufeos.db
del backend\__pycache__ /Q /S
pip install -r requirements.txt
BUFE_BASLAT.bat
```

```bash
# Linux/Mac
cd ~/KucukBufe
rm -f backend/bufeos.db
rm -rf backend/__pycache__
pip3 install -r requirements.txt
./start.sh
```

---

## ✅ Kurulumun Doğru Çalıştığını Anlamak

Sunucu başarıyla başladığında şunu görmelisiniz:

```
========================================
   🏪 BüfeOS Başlatılıyor...
========================================

✅ Veritabanı mevcut.  (veya İlk kurulum...)

🌐 Sunucu başlatılıyor...
📍 Tarayıcınızda açın: http://localhost:8000/templates/index.html

INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## 📞 Hala Sorun mu Var?

### Hata Loglarını Paylaşın

1. Hatayı tam olarak kopyalayın
2. GitHub Issues'da yeni issue açın
3. Şu bilgileri ekleyin:
   - İşletim sistemi (Windows/Mac/Linux)
   - Python sürümü (`python --version`)
   - Hata mesajının tamamı

### Hızlı Test

API'nin çalışıp çalışmadığını test edin:

**Windows (PowerShell):**
```powershell
Invoke-WebRequest -Uri http://localhost:8000/ | Select-Object -ExpandProperty Content
```

**Linux/Mac:**
```bash
curl http://localhost:8000/
```

Beklenen çıktı:
```json
{
  "status": "OK",
  "app": "BüfeOS",
  "version": "1.0.0",
  "message": "Küçük büfeler için stok yönetim sistemi 🏪"
}
```

---

## 🎓 Faydalı Komutlar

### Veritabanını Yedekle

```batch
REM Windows
copy backend\bufeos.db backup\bufeos_%date:~-4,4%%date:~-7,2%%date:~-10,2%.db
```

```bash
# Linux/Mac
cp backend/bufeos.db backup/bufeos_$(date +%Y%m%d).db
```

### Demo Veriyi Yeniden Yükle

```bash
cd backend
rm bufeos.db
python demo_data.py
```

### Sunucuyu Arka Planda Çalıştır (Linux/Mac)

```bash
cd backend
nohup python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
```

---

**İyi kullanımlar! 🏪**
