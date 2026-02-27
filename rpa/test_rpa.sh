#!/bin/bash
# Script de prueba rápida del RPA

echo "🧪 Prueba del RPA - Wikipedia Scraper"
echo "======================================"
echo ""

# Verificar que el backend esté corriendo
echo "1. Verificando backend..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "   ✓ Backend activo"
else
    echo "   ❌ Backend no responde"
    echo "   Inicia el backend con: uvicorn app.main:app --reload"
    exit 1
fi

echo ""
echo "2. Ejecutando RPA..."
echo ""

python wikipedia_scraper.py "https://en.wikipedia.org/wiki/Avengers:_Doomsday"

echo ""
echo "✅ Prueba completada"
echo ""
echo "📁 Revisa la carpeta screenshots/ para ver los resultados"
