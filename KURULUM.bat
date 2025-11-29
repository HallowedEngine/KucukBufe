@echo off
chcp 65001 > nul
color 0A
cls

echo.
echo ═══════════════════════════════════════════════════════
echo    🏪 BüfeOS Otomatik Kurulum Başlatıcı
echo ═══════════════════════════════════════════════════════
echo.
echo    Merhaba! Bu program BüfeOS'u otomatik kuracak.
echo    Hiçbir şey yapmanıza gerek yok, sadece bekleyin!
echo.
echo ═══════════════════════════════════════════════════════
echo.

timeout /t 3 /nobreak > nul

REM ============================================
REM Adım 1: Python Kontrolü
REM ============================================
echo [1/5] Python kontrolü yapılıyor...
python --version >nul 2>&1

if %errorlevel% neq 0 (
    echo.
    echo ❌ Python bulunamadı!
    echo.
    echo Lütfen Python'u indirip kurun:
    echo 👉 https://www.python.org/downloads/
    echo.
    echo ⚠️  Kurulum sırasında "Add Python to PATH" seçeneğini işaretleyin!
    echo.
    echo Kurulumdan sonra bu dosyayı tekrar çalıştırın.
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Python bulundu!
)

echo.

REM ============================================
REM Adım 2: Gerekli Kütüphaneleri Yükle
REM ============================================
echo [2/5] Gerekli programlar yükleniyor... (2-3 dakika sürebilir)
echo      ⏳ Lütfen bekleyin...

pip install -q -r requirements.txt > nul 2>&1

if %errorlevel% neq 0 (
    echo.
    echo ⚠️  İnternet bağlantısı gerekli!
    echo.
    echo Tekrar deneyin...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo.
        echo ❌ Kurulum başarısız! İnternet bağlantınızı kontrol edin.
        pause
        exit /b 1
    )
)

echo ✅ Programlar yüklendi!
echo.

REM ============================================
REM Adım 3: Demo Veri Yükle
REM ============================================
echo [3/5] Demo veriler hazırlanıyor...

cd backend

if not exist "bufeos.db" (
    python demo_data.py > nul 2>&1
    echo ✅ Demo ürünler ve satışlar eklendi!
) else (
    echo ✅ Veritabanı zaten mevcut!
)

cd ..
echo.

REM ============================================
REM Adım 4: Masaüstü Kısayolu Oluştur
REM ============================================
echo [4/5] Masaüstü kısayolları oluşturuluyor...

REM BüfeOS Başlatıcı kısayolu
set DESKTOP=%USERPROFILE%\Desktop
set SCRIPT_DIR=%~dp0

REM VBScript ile kısayol oluştur (Windows'ta standart yöntem)
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%DESKTOP%\BufeOS.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%SCRIPT_DIR%BUFE_BASLAT.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> CreateShortcut.vbs
echo oLink.Description = "BufeOS Stok Yonetim Sistemi" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

cscript //nologo CreateShortcut.vbs
del CreateShortcut.vbs

echo ✅ Masaüstünde "BufeOS" kısayolu oluşturuldu!
echo.

REM ============================================
REM Adım 5: Tarayıcı Kısayolu
REM ============================================
echo [5/5] Tarayıcı kısayolu oluşturuluyor...

REM HTML kısayolu oluştur (tüm tarayıcılarda açılır)
echo ^<!DOCTYPE html^> > "%DESKTOP%\BufeOS Panel.html"
echo ^<html^> >> "%DESKTOP%\BufeOS Panel.html"
echo ^<head^> >> "%DESKTOP%\BufeOS Panel.html"
echo ^<meta http-equiv="refresh" content="0; url=http://localhost:8000/templates/index.html"^> >> "%DESKTOP%\BufeOS Panel.html"
echo ^<title^>BufeOS Panel^</title^> >> "%DESKTOP%\BufeOS Panel.html"
echo ^</head^> >> "%DESKTOP%\BufeOS Panel.html"
echo ^<body^>Yukleniyor...^</body^> >> "%DESKTOP%\BufeOS Panel.html"
echo ^</html^> >> "%DESKTOP%\BufeOS Panel.html"

echo ✅ "BufeOS Panel" kısayolu oluşturuldu!
echo.

REM ============================================
REM KURULUM TAMAMLANDI!
REM ============================================
color 0E
cls
echo.
echo ═══════════════════════════════════════════════════════
echo    ✅ KURULUM TAMAMLANDI!
echo ═══════════════════════════════════════════════════════
echo.
echo    BüfeOS başarıyla kuruldu!
echo.
echo    📁 Masaüstünüzde 2 kısayol oluşturuldu:
echo       1. "BufeOS" - Programı başlatır
echo       2. "BufeOS Panel" - Arayüzü açar
echo.
echo ═══════════════════════════════════════════════════════
echo.
echo    🚀 NASIL KULLANILIR?
echo.
echo    1️⃣  Masaüstünde "BufeOS" kısayoluna çift tıklayın
echo        → Siyah pencere açılacak (KAPATMAYIN!)
echo.
echo    2️⃣  "BufeOS Panel" kısayoluna çift tıklayın
echo        → Tarayıcıda arayüz açılacak
echo.
echo    3️⃣  Kullanmaya başlayın! 🎉
echo.
echo ═══════════════════════════════════════════════════════
echo.
echo    📚 Yardım Dosyaları:
echo       • BUFECI_KILAVUZU.md - Kullanım rehberi
echo       • BASLANGIC_REHBERI.txt - İlk adımlar
echo       • DESTEK_BILGILERI.txt - Sorun çözme
echo.
echo ═══════════════════════════════════════════════════════
echo.

set /p AUTOSTART="Şimdi BüfeOS'u başlatmak ister misiniz? (E/H): "

if /i "%AUTOSTART%"=="E" (
    echo.
    echo 🚀 BüfeOS başlatılıyor...
    echo.
    timeout /t 2 /nobreak > nul
    start "" "%DESKTOP%\BufeOS.lnk"
    timeout /t 3 /nobreak > nul
    start "" "%DESKTOP%\BufeOS Panel.html"
    echo.
    echo ✅ BüfeOS başlatıldı!
    echo    Siyah pencereyi kapatmayın!
    echo.
) else (
    echo.
    echo 👍 Tamam! Daha sonra masaüstünden başlatabilirsiniz.
    echo.
)

echo İyi kullanımlar! 🏪
echo.
pause
