#!/bin/bash
# Script para iniciar el worker de Celery

echo "🔧 Iniciando Celery Worker..."
echo "📦 Importando tareas desde app.tasks..."
celery -A app.celery_app worker --loglevel=info -E
