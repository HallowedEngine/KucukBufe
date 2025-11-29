# 🚀 BüfeOS Production Deployment Rehberi

## Online'a Çıkarma (Railway ile)

**Hedef:** Herkes internetten erişebilsin, gerçek büfeler kullansın!

---

## 📋 Ön Gereksinimler

- ✅ GitHub hesabı
- ✅ Railway hesabı (ücretsiz)
- ✅ Domain (opsiyonel - bufeos.com)

---

## 🛤️ Railway Deployment (Önerilen)

### Adım 1: Railway Hesabı Aç

```
1. https://railway.app adresine git
2. "Login with GitHub" ile giriş yap
3. GitHub'daki projeyi bağlama izni ver
```

### Adım 2: Yeni Proje Oluştur

```
1. Railway dashboard'da "New Project" tıkla
2. "Deploy from GitHub repo" seç
3. "KucukBufe" repository'sini seç
4. Deploy başlayacak!
```

### Adım 3: PostgreSQL Ekle

```
1. Proje sayfasında "+ New" tıkla
2. "Database" → "PostgreSQL" seç
3. Otomatik oluşturulacak
4. DATABASE_URL otomatik environment variable'a eklenecek
```

### Adım 4: Environment Variables

Railway dashboard'da "Variables" sekmesine git:

```bash
# Otomatik eklenenler:
DATABASE_URL=postgresql://...  # Railway ekler

# Manuel eklemen gerekenler:
SECRET_KEY=super-secret-key-buraya-random-string
JWT_SECRET=another-secret-key
ENVIRONMENT=production
```

### Adım 5: Deploy!

```
1. Railway otomatik deploy edecek
2. 2-3 dakika sonra hazır!
3. URL: https://kucukbufe-production.up.railway.app
```

---

## 🌐 Domain Bağlama (bufeos.com)

### Adım 1: Domain Al

```
1. GoDaddy/Hostinger/Cloudflare'den domain al
2. Örn: bufeos.com (yıllık ~100 TL)
```

### Adım 2: Railway'de Domain Ayarla

```
1. Railway dashboard → "Settings" → "Domains"
2. "Custom Domain" tıkla
3. bufeos.com yazıp ekle
4. CNAME kaydını kopyala
```

### Adım 3: DNS Ayarları

Domain sağlayıcında (GoDaddy vb.):

```
Type: CNAME
Name: @  (veya www)
Value: [Railway'den aldığın CNAME]
TTL: 3600
```

30 dakika sonra bufeos.com hazır! 🎉

---

## 🔒 SSL/HTTPS

Railway otomatik SSL sertifikası verir!

✅ https://bufeos.com otomatik çalışacak
✅ Ücretsiz Let's Encrypt sertifikası
✅ Otomatik yenileme

---

## 📊 İlk Deploy Sonrası

### 1. API Test Et

```bash
# Health check
curl https://bufeos.com/

# Beklenen çıktı:
{
  "status": "OK",
  "app": "BüfeOS",
  "version": "2.0.0 (Multi-Tenant)",
  "message": "Production-ready! 🚀"
}
```

### 2. İlk Kullanıcı Oluştur

Tarayıcıda:
```
https://bufeos.com/templates/register.html
```

Form doldur:
- Büfe Adı: Test Büfesi
- Email: test@test.com
- Username: test
- Şifre: test123

Kayıt ol → 30 gün ücretsiz deneme başlar!

### 3. Login Yap

```
https://bufeos.com/templates/login.html
```

Username: test
Şifre: test123

→ Ana panele yönlendirileceksin!

---

## 🔐 Production Güvenlik

### 1. Secret Keys Değiştir

`.env` dosyasında:

```bash
# Rastgele string oluştur:
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Çıktıyı SECRET_KEY'e yaz
SECRET_KEY=your-generated-secret-here
```

### 2. CORS Ayarları

`backend/main_v2.py` içinde:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://bufeos.com",
        "https://www.bufeos.com"
    ],  # * yerine sadece kendi domain'in
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Rate Limiting (Gelecek)

DDoS koruması için slowapi ekle:

```python
pip install slowapi
```

---

## 💰 Maliyet

### Railway Ücretsiz Plan:
- ✅ $5 ücretsiz kredi/ay
- ✅ 500 saat çalışma
- ✅ PostgreSQL dahil
- ✅ SSL dahil

**Yeterli mi?**
- İlk 10-50 kullanıcı için EVET
- Daha fazla için: $5/ay (Hobby plan)

### Ölçek:
| Kullanıcı | Plan | Maliyet |
|-----------|------|---------|
| 1-50 | Ücretsiz | $0 |
| 50-500 | Hobby | $5/ay |
| 500+ | Pro | $20/ay |

---

## 📱 PWA (Telefona Yüklenebilir)

### 1. manifest.json Oluştur

`static/manifest.json`:

```json
{
  "name": "BüfeOS",
  "short_name": "BüfeOS",
  "description": "Küçük büfeler için stok yönetimi",
  "start_url": "/templates/index.html",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#3B82F6",
  "icons": [
    {
      "src": "/static/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/static/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### 2. HTML'e Ekle

Tüm HTML sayfalarına ekle:

```html
<link rel="manifest" href="/static/manifest.json">
<meta name="theme-color" content="#3B82F6">
<link rel="apple-touch-icon" href="/static/icon-192.png">
```

### 3. Service Worker (Gelecek)

Offline çalışma için.

---

## 🎯 İlk Kullanıcıları Getir

### 1. Landing Page

`bufeos.com` → Kayıt sayfası

```
Başlık: Büfenizi Dijitalleştirin!
Alt Başlık: 30 gün ücretsiz deneyin
CTA: Hemen Kayıt Ol →
```

### 2. Sosyal Medya

```
Facebook grupları:
- Büfe Sahipleri
- Esnaf Grupları

Instagram:
- @bufeos
- Büfe fotoğrafları + screenshot
```

### 3. Direkt Satış

İlk 10 büfeyi sen kur:
1. Büfeye git
2. Sistemi göster (telefonda)
3. Kayıt yap (yerinde)
4. 5 dakikada kullanmaya başlasın

---

## 📊 Monitoring & Analytics

### 1. Railway Logs

```
Railway dashboard → Logs
Real-time hata takibi
```

### 2. User Analytics (Future)

```python
pip install mixpanel
```

Track:
- Kayıt sayısı
- Aktif kullanıcı
- Satış sayısı

### 3. Error Tracking

```python
pip install sentry-sdk
```

Gerçek zamanlı hata bildirimleri.

---

## 🔄 Otomatik Deployment

Her git push'da otomatik deploy:

```bash
git add .
git commit -m "feat: yeni özellik"
git push origin main

# Railway otomatik deploy edecek (2-3 dk)
```

---

## 💳 Ödeme Sistemi (Future)

### Stripe Entegrasyonu:

```python
pip install stripe
```

```python
# Aylık abonelik
price_id = "price_monthly_99tl"

# Checkout session
checkout_session = stripe.checkout.Session.create(
    customer_email=user.email,
    mode="subscription",
    line_items=[{"price": price_id, "quantity": 1}],
    success_url="https://bufeos.com/success",
    cancel_url="https://bufeos.com/cancel"
)
```

---

## 📞 Destek Sistemi

### 1. Email Notifications

```python
pip install fastapi-mail
```

Gönder:
- Kayıt onayı
- Trial bitiş uyarısı (5 gün kala)
- Ödeme hatırlatması

### 2. WhatsApp Bot (Future)

Twilio API ile:
- Stok uyarıları
- Günlük rapor
- Sipariş listesi

---

## ✅ Production Checklist

Canlıya almadan önce:

- [ ] PostgreSQL bağlantısı çalışıyor
- [ ] SECRET_KEY değiştirildi
- [ ] CORS sadece kendi domain
- [ ] SSL aktif (https://)
- [ ] İlk kullanıcı kayıt oldu ve test etti
- [ ] Email bildirimleri çalışıyor (future)
- [ ] Backup sistemi var (Railway otomatik)
- [ ] Domain bağlandı (bufeos.com)
- [ ] PWA manifest eklendi
- [ ] Google Analytics eklendi (future)

---

## 🚀 Sonraki Adımlar

1. **İlk 10 Kullanıcı:** Elle kur, feedback al
2. **Landing Page:** Marketing sitesi yap
3. **Ödeme:** Stripe entegre et
4. **Mobil App:** React Native (future)
5. **API v3:** GraphQL (future)

---

**Tebrikler! BüfeOS artık online! 🎉**

**URL:** https://bufeos.com
**Admin:** sen
**İlk kullanıcılar:** geliyorlar! 🚀
