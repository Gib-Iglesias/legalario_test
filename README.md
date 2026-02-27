# 💰 Transactions App - Full Stack Project

Sistema completo de gestión de transacciones con procesamiento asíncrono, notificaciones en tiempo real, asistente de IA y automatización RPA.

## 🎯 Características Principales

- **Backend FastAPI**: API REST con procesamiento asíncrono
- **Frontend React**: Interfaz moderna con actualizaciones en tiempo real
- **Integración OpenAI**: Generación de resúmenes con IA
- **RPA Playwright**: Automatización de scraping web

## 🏗️ Tecnologías

### Backend

- FastAPI (API REST)
- SQLAlchemy (ORM)
- Celery + Redis (Procesamiento asíncrono)
- WebSocket (Tiempo real)
- OpenAI API (IA)
- PostgreSQL/SQLite (Base de datos)

### Frontend

- React 18
- Vite
- WebSocket API
- CSS Modules

### RPA

- Playwright
- Chromium

## 📋 Requisitos

- Python 3.8+
- Node.js 16+
- Docker (para Redis)

## 🚀 Inicio Rápido

Ver el archivo **INSTALACION.md** para instrucciones detalladas paso a paso.

### Resumen

```bash
# 1. Instalar dependencias
cd backend && pip install -r requirements.txt
cd ../frontend && npm install
cd ../rpa && pip install -r requirements.txt && playwright install chromium

# 2. Iniciar servicios (4 terminales)
# Terminal 1: cd backend && docker-compose up redis
# Terminal 2: cd backend && ./start_worker.sh
# Terminal 3: cd backend && uvicorn app.main:app --reload
# Terminal 4: cd frontend && npm run dev

# 3. Abrir http://localhost:5173
```

## 📚 Documentación

- **README.md** (este archivo) - Visión general del proyecto
- **ARQUITECTURA.md** - Arquitectura técnica y formato del código
- **INSTALACION.md** - Guía paso a paso para levantar el proyecto

## 🎯 Funcionalidades

### 1. Gestión de Transacciones

- Crear transacciones (idempotente)
- Procesar asíncronamente con Celery
- Listar y filtrar transacciones
- Estadísticas en tiempo real

### 2. Notificaciones en Tiempo Real

- WebSocket para actualizaciones instantáneas
- Notificaciones visuales tipo toast
- Sincronización entre múltiples clientes

### 3. Asistente de IA

- Generar resúmenes de texto con OpenAI
- Modo mock para desarrollo sin API key
- Registro de peticiones y tokens

### 4. RPA (Automatización)

- Scraping de Wikipedia con Playwright
- Screenshots automáticos
- Integración con asistente de IA
- Resultados en JSON

## 🌐 URLs

- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📊 Endpoints API

### Transacciones

- `POST /transactions/create` - Crear transacción
- `POST /transactions/async-process` - Procesar asíncronamente
- `GET /transactions/list` - Listar transacciones
- `GET /transactions/{id}` - Obtener transacción
- `WS /transactions/stream` - WebSocket tiempo real
- `GET /transactions/stats` - Estadísticas

### Asistente IA

- `POST /assistant/summarize` - Generar resumen
- `GET /assistant/summaries` - Listar resúmenes
- `GET /assistant/summaries/{id}` - Obtener resumen
- `GET /assistant/stats` - Estadísticas del asistente

## 🧪 Pruebas

### Backend

```bash
cd backend
python test_api.py          # Pruebas de transacciones
python test_async.py        # Pruebas de procesamiento asíncrono
python test_websocket.py    # Pruebas de WebSocket
python test_openai.py       # Pruebas de IA
```

### RPA

```bash
cd rpa
python wikipedia_scraper.py  # Scraping básico
python advanced_scraper.py   # Scraping avanzado
python run_examples.py       # Múltiples ejemplos
```

## 🔧 Configuración

### Variables de Entorno (.env)

```bash
# Backend
DATABASE_URL=postgresql://user:password@localhost:5432/transactions_db
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=your-api-key-here-or-mock
```

### Modo Mock (sin API key de OpenAI)

El sistema funciona perfectamente sin API key de OpenAI usando un modo mock para desarrollo.

## 📁 Estructura del Proyecto

```
.
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── routers/     # Endpoints
│   │   ├── services/    # Lógica de negocio
│   │   ├── models.py    # Modelos de BD
│   │   └── main.py      # Aplicación principal
│   ├── requirements.txt
│   └── docker-compose.yml
├── frontend/            # Aplicación React
│   ├── src/
│   │   ├── components/  # Componentes React
│   │   ├── hooks/       # Hooks personalizados
│   │   └── App.jsx      # Componente principal
│   └── package.json
├── rpa/                 # Scripts de automatización
│   ├── wikipedia_scraper.py
│   ├── advanced_scraper.py
│   └── requirements.txt
├── README.md            # Este archivo
├── ARQUITECTURA.md      # Documentación técnica
└── INSTALACION.md       # Guía de instalación
```

---
