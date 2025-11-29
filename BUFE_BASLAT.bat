@echo off
chcp 65001 > nul
cls

echo.
echo ========================================
echo    🏪 BüfeOS Başlatılıyor...
echo ========================================
echo.

cd backend

REM Veritabanı kontrolü - İlk açılış
if not exist "bufeos.db" (
    echo 📦 İlk kurulum tespit edildi!
    echo 📊 Demo veri yükleniyor...
    python demo_data.py
    echo.
    echo ✅ Demo veriler yüklendi!
    echo.

    REM İlk açılışta hoş geldiniz sayfasını işaretle
    echo first_time > .first_launch
) else (
    echo ✅ Veritabanı mevcut.
    echo.
)

echo 🌐 Sunucu başlatılıyor...
echo 📍 Tarayıcınızda açın: http://localhost:8000/templates/index.html
echo.
echo ⚠️  Durdurmak için: Ctrl+C
echo.
echo ========================================
echo.

REM Uvicorn ile sunucuyu başlat
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause
