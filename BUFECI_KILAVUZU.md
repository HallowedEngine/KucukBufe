# 🏪 BüfeOS Kullanım Kılavuzu - Büfeciler İçin

**Hoş geldiniz!** Bu kılavuz teknik bilgi gerektirmez. Simit satmak kadar basit! 😊

---

## 📱 Hızlı Başlangıç (İlk 5 Dakika)

### 1. Programı Başlatın

**Masaüstünde "BüfeOS" simgesini bulun**

Veya:
- `BUFE_BASLAT.bat` dosyasına çift tıklayın

**Ne göreceksiniz:**
```
========================================
   🏪 BüfeOS Başlatılıyor...
========================================
✅ Veritabanı mevcut.
🌐 Sunucu başlatılıyor...
```

✅ **Hazır!** Siyah pencereyi kapatmayın!

---

### 2. Tarayıcıda Açın

**Google Chrome veya başka bir tarayıcıyı açın**

Adres çubuğuna yazın:
```
localhost:8000/templates/index.html
```

**İPUCU:** Bu adresi favorilere ekleyin! 🔖

---

## 🎯 Ana Sayfa - Her Sabah İlk Bakacağınız Yer

### 💰 Bugünkü Satış Kartı

```
💰 Bugünkü Satış
2,450 TL (↑ %15 dünden fazla)
Kar: 680 TL
```

**Ne anlama geliyor?**
- **2,450 TL:** Bugün şu ana kadar sattığınız toplam
- **↑ %15:** Dünden %15 daha fazla satış yaptınız (iyi gidiyor!)
- **Kar: 680 TL:** Bugün cebinize kalan para

---

### ⚠️ Az Kalanlar Kartı

```
⚠️ Az Kalanlar
- Marlboro: 3 paket kaldı
- Su 0.5L: 8 şişe kaldı
- Simit: Bitti! (Sipariş ver)
```

**Ne yapmalısınız?**
1. Sabah açılışta buraya bakın
2. "Bitti!" yazanları not edin
3. Toptancınıza sipariş verin

**İPUCU:** "Sipariş Listesi" sayfası size tam listeyi WhatsApp'tan gönderiyor! (Aşağıda anlatıldı)

---

### 🔥 En Çok Satanlar

```
🔥 En Çok Satanlar (Bugün)
1. Simit - 45 adet
2. Su 0.5L - 38 adet
3. Ayran - 28 adet
```

**Ne işe yarar?**
- Hangi ürünleri daha çok stoklamalısınız
- Hangi ürünleri rafa öne koymalısınız
- Hangi ürünlerden daha fazla sipariş vermelisiniz

---

## 💸 Hızlı Satış - Her Müşteri Geldiğinde

### Adım Adım Satış Yapma

**1. "Hızlı Satış" butonuna tıklayın** (Üstteki menüden)

**2. Müşteri ne istedi?**

#### Seçenek A: Barkodlu Ürün (Sigara, kola, vb.)
1. Barkod alanına tıklayın
2. Barkod okuyucuyla okutun
3. **Enter** tuşuna basın
4. ✅ Otomatik sepete eklendi!

#### Seçenek B: Barkodlu Olmayan (Simit, poğaça, vb.)
1. Kategori seçin: **🥖 Ekmek**
2. Ürüne dokunun: **Simit**
3. ✅ Sepete eklendi!

**3. Sepeti Kontrol Edin**

```
🛒 Sepet
- Simit x 2 = 10 TL
- Su 0.5L x 1 = 3 TL
Toplam: 13 TL
```

**Adet yanlışsa:**
- **+** butonu → Adet artır
- **-** butonu → Adet azalt
- **🗑️** butonu → Sepetten çıkar

**4. "Satışı Tamamla" Butonuna Basın**

✅ **Bitti!** Stok otomatik azaldı, satış kaydedildi!

---

## 📦 Ürünlerinizi Ekleyin

### İlk Kurulum: Ürünlerinizi Sisteme Yükleyin

**2 Yöntem Var:**

---

### Yöntem 1: Tek Tek Ekleme (10-20 ürünse)

**1. "Ürünler" sayfasına gidin**

**2. "Yeni Ürün Ekle" butonuna basın**

**3. Formu doldurun:**

```
Ürün Adı: Simit *
Barkod: 8690123456 (varsa)
Kategori: Ekmek *
Stok: 50 *
Alış Fiyatı: 3.0 *
Satış Fiyatı: 5.0 *
```

**4. "Ürün Ekle" butonuna basın**

✅ Ürün eklendi!

---

### Yöntem 2: Excel ile Toplu Yükleme (50+ ürünse) ⭐ ÖNERİLEN

**1. Excel'i açın**

**2. Şu şekilde liste yapın:**

| urun_adi | barkod | stok | satis_fiyat | alis_fiyat | kategori |
|----------|--------|------|-------------|------------|----------|
| Simit | 8690123456 | 50 | 5.0 | 3.0 | Ekmek |
| Su 0.5L | 8690123457 | 100 | 3.0 | 1.5 | İçecek |
| Marlboro | 8690123458 | 20 | 55.0 | 48.0 | Sigara |

**3. "Farklı Kaydet" → "CSV (Virgülle Ayrılmış)"**

**4. BüfeOS'ta "CSV Yükle" butonuna basın**

**5. Dosyanızı seçin**

✅ **30 saniyede 50 ürün yüklendi!**

---

## 📋 Sipariş Listesi - En Sevilen Özellik!

### Toptancınıza WhatsApp'tan Sipariş Gönderin

**1. "Sipariş Listesi" sayfasına gidin**

**2. Sistem size şunu gösterir:**

```
📋 SİPARİŞ LİSTESİ (28.11.2024)

🚬 Sigara
  • Marlboro: 20 adet (3 kaldı)
  • Winston: 20 adet (6 kaldı)

🥤 İçecek
  • Su 0.5L: 100 adet (8 kaldı)
  • Simit: 50 adet (Bitti!)

Toplam 15 çeşit ürün
```

**3. "WhatsApp'a Kopyala" butonuna basın**

**4. WhatsApp'ı açın**

**5. Toptancınızı seçin**

**6. Yapıştır (CTRL+V)** → Gönder!

✅ **10 saniyede sipariş verdiniz!**

---

## 📊 Stok Güncelleme

### Mal Aldığınızda Stoku Artırın

**1. "Ürünler" sayfasına gidin**

**2. Ürünü bulun** (Arama kutusuna yazabilirsiniz)

**3. ✏️ (Kalem) ikonuna tıklayın**

**4. Yeni stok adedini yazın**

Örnek:
- Eski stok: 5
- Aldığınız: 20
- Yeni stok: **25** yazın

**5. Enter'a basın**

✅ Stok güncellendi!

---

## 💡 İpuçları & Püf Noktaları

### 🌅 Sabah Rutini (5 dakika)

1. ☕ Kahve alın
2. 💻 BüfeOS'u açın
3. 👀 "Az Kalanlar" kartına bakın
4. 📋 "Sipariş Listesi"nden WhatsApp'a gönderin
5. ✅ Günü başlatın!

---

### 🌙 Akşam Rutini (2 dakika)

1. 💰 "Bugünkü Satış" kartına bakın
2. 📊 Ne kadar kazandınız?
3. 🔥 "En Çok Satanlar"a bakın
4. 🛏️ Rahat uyuyun (sayım yok!)

---

### 📱 Telefondan Kullanma

**Mobilden erişim:**

1. Bilgisayarınızın IP adresini öğrenin:
   - Windows: `ipconfig` yazın
   - IP: 192.168.1.100 gibi bir şey

2. Telefonunuzda tarayıcıyı açın

3. Şunu yazın:
   ```
   192.168.1.100:8000/templates/index.html
   ```

4. **Ana ekrana ekle** → Artık uygulama gibi!

---

### 💾 Yedekleme (Haftada 1)

**ÖNEMLİ:** Verilerinizi kaybetmeyin!

**Adım 1:** `backend` klasörünü açın

**Adım 2:** `bufeos.db` dosyasını bulun

**Adım 3:** Sağ tık → Kopyala

**Adım 4:** `backup` klasörüne yapıştır

**Adım 5:** Adını değiştir: `bufeos_28112024.db`

✅ Yedek alındı!

---

## ❓ Sık Sorulan Sorular

### S: İnternet olmadan çalışır mı?
**C:** EVET! Tamamen offline çalışır. İnternet gerektirmez.

---

### S: Bilgisayarım bozulursa verilerim kaybolur mu?
**C:** Hayır, eğer yedek aldıysanız. Haftada 1 kere `bufeos.db` dosyasını USB'ye kopyalayın.

---

### S: Telefonda kullanabilir miyim?
**C:** Evet! Yukarıdaki "Telefondan Kullanma" bölümüne bakın.

---

### S: Satışı yanlış kaydettim, nasıl düzeltebilirim?
**C:** Şu an manuel düzeltme yok. Sonraki güncellemede "İptal" özelliği gelecek. Notunuza yazıp sonra düzeltin.

---

### S: Başka büfede de kullanabilir miyim?
**C:** Her büfe için ayrı lisans gerekiyor. Ama ikinci büfeye %50 indirim var!

---

### S: Sistemde sorun çıkarsa kimden yardım alırım?
**C:** Beni arayın: [TELEFON NUMARANIZ]
WhatsApp: [WHATSAPP NUMARANIZ]

---

## 🆘 Sorun mu Var?

### Sorun: "Sayfa açılmıyor"

✅ **Çözüm:**
1. Siyah pencere (komut satırı) açık mı? Kapalıysa `BUFE_BASLAT.bat`'ı başlatın
2. Doğru URL'i yazdınız mı? `localhost:8000/templates/index.html`

---

### Sorun: "Ürün stokta yok diyor ama var"

✅ **Çözüm:**
1. "Ürünler" sayfasına gidin
2. Stok sayısını kontrol edin
3. Yanlışsa güncelleyin

---

### Sorun: "Sistem yavaş"

✅ **Çözüm:**
1. Tarayıcıyı kapatıp yeniden açın
2. Bilgisayarı yeniden başlatın
3. Hala yavaşsa beni arayın!

---

## 📞 İletişim & Destek

**Geliştirici:**
- Ad: [ADINIZ]
- Telefon: [NUMARANIZ]
- WhatsApp: [WHATSAPP]
- E-posta: [EMAIL]

**Destek Saatleri:**
- Hafta içi: 09:00 - 18:00
- Hafta sonu: Sadece acil durumlar

---

## 🎓 Video Eğitimler (Yakında)

- [ ] İlk Kurulum (5 dk)
- [ ] Ürün Ekleme (3 dk)
- [ ] Hızlı Satış (2 dk)
- [ ] Sipariş Listesi (2 dk)

---

**BüfeOS'u kullandığınız için teşekkürler! Kolay gelsin! 🏪**

**Sorularınız varsa çekinmeden arayın!**
