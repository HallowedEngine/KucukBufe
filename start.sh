#!/bin/bash

echo "🚀 BüfeOS Başlatılıyor..."
echo ""

# Backend klasörüne git
cd backend

# Veritabanını kontrol et
if [ ! -f "bufeos.db" ]; then
    echo "📦 İlk kurulum tespit edildi!"
    echo "📊 Demo veri yükleniyor..."
    python demo_data.py
    echo ""
else
    echo "✅ Veritabanı mevcut."
    echo ""
fi

echo "🌐 Sunucu başlatılıyor..."
echo "📍 Tarayıcınızda açın: http://localhost:8000/templates/index.html"
echo ""
echo "⚠️  Durdurmak için: Ctrl+C"
echo ""

# Uvicorn ile sunucuyu başlat
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
