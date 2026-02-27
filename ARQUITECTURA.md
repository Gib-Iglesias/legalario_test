# 🏗️ Arquitectura del Sistema

## Visión General

Sistema full-stack con arquitectura de microservicios que incluye:

- API REST con FastAPI
- Frontend SPA con React
- Procesamiento asíncrono con Celery
- Comunicación en tiempo real con WebSocket
- Integración con IA (OpenAI)
- Automatización RPA (Playwright)

## 📐 Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                             │
│                    React + WebSocket                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Transaction  │  │ Notifications │  │  Summary     │       │
│  │    Form      │  │   System     │  │    Tool      │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTP REST + WebSocket
                 ↓
┌─────────────────────────────────────────────────────────────┐
│                        BACKEND                              │
│                    FastAPI + Celery                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Transactions │  │   Assistant  │  │   Internal   │       │
│  │   Router     │  │    Router    │  │    Router    │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                 │               │
│  ┌──────▼─────────────────▼────────────-────▼──────-─┐      │
│  │           WebSocket Manager                       │      │
│  └───────────────────────────────────────────────────┘      │
└────┬──────────────────┬──────────────────┬────────────────-─┘
     │                  │                  │
     ↓                  ↓                  ↓
┌─────────┐      ┌──────────┐      ┌──────────┐
│PostgrSQL│      │  Redis   │      │  OpenAI  │
│   BD    │      │  Queue   │      │   API    │
└─────────┘      └────┬─────┘      └──────────┘
     ↑                │
     │                ↓
     │         ┌──────────┐
     │         │  Celery  │
     │         │  Worker  │
     │         └────┬─────┘
     │              │
     └──────────────┘
                    ↑
                    │ Envía resultados
                    │
┌─────────────────────────────────────────────────────────────┐
│                          RPA                                │
│                   Playwright + Python                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Chromium   │→ │   Scraper    │→ │  API Client  │       │
│  │   Browser    │  │   Logic      │  │              │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Flujos de Datos

### 1. Flujo de Transacción Completa

```
Usuario → Frontend → POST /transactions/create → Backend
                                                    ↓
                                            Guarda en BD
                                                    ↓
                                            WebSocket notifica
                                                    ↓
                                            Frontend actualiza
                                                    ↓
Usuario hace clic "Procesar" → POST /transactions/async-process
                                                    ↓
                                            Encola en Redis
                                                    ↓
                                            Worker procesa
                                                    ↓
                                            Actualiza BD
                                                    ↓
                                            WebSocket notifica
                                                    ↓
                                            Frontend actualiza
```

### 2. Flujo de Resumen con IA

```
Usuario → Frontend → POST /assistant/summarize → Backend
                                                    ↓
                                            Crea registro en BD
                                                    ↓
                                            OpenAI Service
                                                    ↓
                                            GPT-3.5-turbo (o mock)
                                                    ↓
                                            Actualiza registro
                                                    ↓
                                            Retorna resumen
                                                    ↓
                                            Frontend muestra
```

### 3. Flujo RPA Completo

```
RPA Script → Playwright → Wikipedia
                            ↓
                    Extrae contenido
                            ↓
                    Toma screenshot
                            ↓
            POST /assistant/summarize → Backend
                                          ↓
                                    Procesa con IA
                                          ↓
                                    Guarda en BD
                                          ↓
                                    Retorna resumen
                                          ↓
                            RPA guarda JSON
```

## 🗄️ Modelo de Datos

### Tabla: transactions

```sql
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    monto FLOAT NOT NULL,
    tipo VARCHAR NOT NULL,
    estado VARCHAR DEFAULT 'pendiente',
    idempotency_key VARCHAR UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

### Tabla: summary_requests

```sql
CREATE TABLE summary_requests (
    id SERIAL PRIMARY KEY,
    original_text TEXT NOT NULL,
    summary TEXT,
    model_used VARCHAR,
    tokens_used INTEGER,
    status VARCHAR DEFAULT 'pending',
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);
```

## 🔌 APIs y Endpoints

### REST API

| Método | Endpoint                      | Descripción             |
| ------ | ----------------------------- | ----------------------- |
| POST   | `/transactions/create`        | Crear transacción       |
| POST   | `/transactions/async-process` | Procesar asíncronamente |
| GET    | `/transactions/list`          | Listar transacciones    |
| GET    | `/transactions/{id}`          | Obtener transacción     |
| GET    | `/transactions/stats`         | Estadísticas            |
| POST   | `/assistant/summarize`        | Generar resumen         |
| GET    | `/assistant/summaries`        | Listar resúmenes        |
| GET    | `/assistant/stats`            | Estadísticas IA         |

### WebSocket

| Endpoint                  | Descripción                   |
| ------------------------- | ----------------------------- |
| `WS /transactions/stream` | Notificaciones en tiempo real |

## 🎨 Componentes Frontend

### Estructura de Componentes

```
App
├── Header
│   └── WebSocketStatus
├── Notifications (Toast)
├── Grid
│   ├── Column Left
│   │   ├── TransactionForm
│   │   └── Stats
│   └── Column Right
│       └── TransactionList
└── SummaryTool
```

### Hooks Personalizados

- **useWebSocket**: Gestión de conexión WebSocket con reconexión automática

## 🔧 Servicios Backend

### OpenAIService

```python
class OpenAIService:
    def __init__(self, api_key: Optional[str])
    async def summarize(self, text: str) -> Dict
    def _mock_summarize(self, text: str) -> Dict
```

**Modos:**

- **Real**: GPT-3.5-turbo con API key
- **Mock**: Para generar resúmenes básicos sin API key

### WebSocket Manager

```python
class ConnectionManager:
    def __init__(self)
    async def connect(self, websocket: WebSocket, user_id: str)
    def disconnect(self, websocket: WebSocket, user_id: str)
    async def broadcast(self, message: dict)
    async def notify_transaction_change(self, transaction_data: dict)
```

## 🔄 Procesamiento Asíncrono

### Celery Tasks

```python
@celery_app.task(name="process_transaction")
def process_transaction(transaction_id: int):
    # 1. Obtener transacción de BD
    # 2. Simular procesamiento (2-5 seg)
    # 3. Actualizar estado (procesado/fallido)
    # 4. Notificar vía WebSocket
```

### Cola Redis

- **Broker**: Redis
- **Backend**: Redis
- **Serializer**: JSON
- **Timezone**: UTC

## 🤖 RPA Architecture

### WikipediaScraper

```python
class WikipediaScraper:
    def scrape_wikipedia(self, url: str) -> dict
    def send_to_summarizer(self, text: str) -> dict
    def run(self, url: str) -> dict
```

**Proceso:**

1. Lanzar Chromium con Playwright
2. Navegar a URL
3. Extraer contenido con JavaScript
4. Tomar screenshot
5. Enviar a API
6. Guardar resultado

## 🔐 Seguridad

### Idempotencia

- Header `X-Idempotency-Key`
- Campo `idempotency_key` en body
- Generación automática con hash SHA256

### CORS

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📊 Patrones de Diseño

### Backend

- **Repository Pattern**: Acceso a datos
- **Service Layer**: Lógica de negocio
- **Dependency Injection**: FastAPI Depends
- **Observer Pattern**: WebSocket notifications

### Frontend

- **Component Pattern**: React components
- **Custom Hooks**: Lógica reutilizable
- **State Management**: useState + useEffect
- **Event-Driven**: WebSocket events

## 🚀 Escalabilidad

### Horizontal Scaling

- **Backend**: Múltiples instancias de FastAPI
- **Workers**: Múltiples workers de Celery
- **Frontend**: CDN para assets estáticos

### Vertical Scaling

- **Database**: PostgreSQL con índices
- **Redis**: Configuración de memoria
- **Workers**: Ajuste de concurrencia

## 📈 Monitoreo

### Métricas Disponibles

- Total de transacciones
- Transacciones por estado
- Transacciones por tipo
- Conexiones WebSocket activas
- Tokens de IA consumidos
- Peticiones al asistente

### Endpoints de Stats

- `GET /transactions/stats`
- `GET /assistant/stats`

## 🔄 Estados de Transacción

```
PENDIENTE → (Worker procesa) → PROCESADO
                             ↘ FALLIDO (10% probabilidad)
```

## 🎯 Formato de Mensajes

### WebSocket Message

```json
{
  "type": "transaction_update",
  "data": {
    "id": 1,
    "user_id": "user123",
    "monto": 100.5,
    "tipo": "deposito",
    "estado": "procesado",
    "created_at": "2024-02-26T18:00:00",
    "updated_at": "2024-02-26T18:00:05"
  },
  "timestamp": "2024-02-26T18:00:05"
}
```

### API Response

```json
{
  "id": 1,
  "user_id": "user123",
  "monto": 100.5,
  "tipo": "deposito",
  "estado": "procesado",
  "created_at": "2024-02-26T18:00:00",
  "updated_at": "2024-02-26T18:00:05"
}
```

## 🛠️ Tecnologías y Versiones

| Tecnología | Versión   | Propósito         |
| ---------- | --------- | ----------------- |
| Python     | 3.8+      | Backend           |
| FastAPI    | 0.109.0   | Framework web     |
| SQLAlchemy | 2.0.36    | ORM               |
| Celery     | 5.3.6     | Tareas asíncronas |
| Redis      | 7-alpine  | Cola y cache      |
| PostgreSQL | 15-alpine | Base de datos     |
| Node.js    | 16+       | Frontend          |
| React      | 18.2.0    | UI Framework      |
| Vite       | 5.1.0     | Build tool        |
| Playwright | 1.41.0    | RPA               |
| OpenAI     | 1.12.0    | IA                |

## 📝 Convenciones de Código

### Python (Backend)

- **Style Guide**: PEP 8
- **Naming**: snake_case para funciones y variables
- **Classes**: PascalCase
- **Async**: Usar async/await para operaciones I/O

### JavaScript (Frontend)

- **Style Guide**: Airbnb
- **Naming**: camelCase para funciones y variables
- **Components**: PascalCase
- **Hooks**: Prefijo "use"

---
