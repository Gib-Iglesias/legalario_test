#!/bin/bash
# Script para ejecutar el servidor de desarrollo

echo "🚀 Iniciando servidor FastAPI..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
