# 🚀 Guía de Instalación - Paso a Paso

Esta guía te llevará desde cero hasta tener el sistema completo funcionando.

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.8 o superior**

  ```bash
  python --version
  ```

- **Node.js 16 o superior**

  ```bash
  node --version
  ```

- **Docker** (para Redis)

  ```bash
  docker --version
  ```

- **Git**
  ```bash
  git --version
  ```

---

## 📦 PARTE 1: Instalación del Backend

### Paso 1.1: Navegar al directorio del backend

```bash
cd backend
```

### Paso 1.2: Crear entorno virtual de Python

```bash
python -m venv venv
```

### Paso 1.3: Activar el entorno virtual

**En macOS/Linux:**

```bash
source venv/bin/activate
```

**En Windows:**

```bash
venv\Scripts\activate
```

Deberías ver `(venv)` al inicio de tu línea de comando.

### Paso 1.4: Instalar dependencias

```bash
pip install -r requirements.txt
```

Esto instalará:

- FastAPI
- SQLAlchemy
- Celery
- Redis
- OpenAI
- Y otras dependencias

### Paso 1.5: Configurar variables de entorno (opcional)

```bash
cp .env.example .env
```

Edita `.env` si quieres usar PostgreSQL o API key de OpenAI:

```bash
# Para desarrollo, puedes dejar estos valores por defecto
DATABASE_URL=sqlite:///./transactions.db
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=mock  # o tu API key real
```

**Nota:** El sistema funciona perfectamente con SQLite y modo mock de OpenAI.

### Paso 1.6: Verificar instalación

```bash
python -c "import fastapi; print('FastAPI instalado correctamente')"
```

---

## 📦 PARTE 2: Instalación del Frontend

### Paso 2.1: Navegar al directorio del frontend

```bash
cd ../frontend
```

### Paso 2.2: Instalar dependencias de Node

```bash
npm install
```

Esto instalará:

- React
- Vite
- Y otras dependencias

### Paso 2.3: Verificar instalación

```bash
npm list react
```

---

## 📦 PARTE 3: Instalación del RPA (Opcional)

### Paso 3.1: Navegar al directorio del RPA

```bash
cd ../rpa
```

### Paso 3.2: Crear entorno virtual

```bash
python -m venv venv
```

### Paso 3.3: Activar el entorno virtual

**En macOS/Linux:**

```bash
source venv/bin/activate
```

**En Windows:**

```bash
venv\Scripts\activate
```

### Paso 3.4: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 3.5: Instalar navegadores de Playwright

```bash
playwright install chromium
```

Esto descargará el navegador Chromium (~100MB).

---

## 🚀 EJECUCIÓN DEL SISTEMA

Ahora que todo está instalado, vamos a levantar el sistema. Necesitarás **4 terminales abiertas**.

### Terminal 1: Redis (Base de datos en memoria)

```bash
cd backend
docker-compose up redis
```

**Espera a ver:**

```
redis_1  | Ready to accept connections
```

**Mantén esta terminal abierta.**

---

### Terminal 2: Worker de Celery (Procesamiento asíncrono)

**Abre una nueva terminal:**

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
./start_worker.sh
```

**O manualmente:**

```bash
celery -A app.celery_app worker --loglevel=info
```

**Espera a ver:**

```
celery@hostname ready.
```

**Mantén esta terminal abierta.**

---

### Terminal 3: Backend API (FastAPI)

**Abre una nueva terminal:**

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Espera a ver:**

```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Mantén esta terminal abierta.**

---

### Terminal 4: Frontend (React)

**Abre una nueva terminal:**

```bash
cd frontend
npm run dev
```

**Espera a ver:**

```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

**Mantén esta terminal abierta.**

---

## ✅ Verificación del Sistema

### 1. Verificar Backend

Abre tu navegador en: **http://localhost:8000/docs**

Deberías ver la documentación interactiva de Swagger.

### 2. Verificar Frontend

Abre tu navegador en: **http://localhost:5173**

Deberías ver:

- Header con "Transactions App"
- Indicador de WebSocket en **verde** (Conectado)
- Formulario de creación de transacciones
- Lista de transacciones (vacía inicialmente)
- Herramienta de resumen con IA

### 3. Verificar WebSocket

En el frontend, el indicador en el header debe mostrar:

```
🟢 Conectado
```

Si muestra "Desconectado", verifica que el backend esté corriendo.

---

## 🎯 Primera Prueba Completa

### Prueba 1: Crear y Procesar una Transacción

1. **En el frontend (http://localhost:5173):**

2. **Completa el formulario:**
   - Usuario ID: `test_user`
   - Monto: `100.50`
   - Tipo: `deposito`

3. **Haz clic en "Crear Transacción"**
   - Verás una notificación verde
   - La transacción aparecerá en la lista con estado "pendiente"

4. **Haz clic en "⚡ Procesar"**
   - Verás una notificación amarilla "encolada"
   - Espera 2-5 segundos

5. **Observa la actualización automática:**
   - El estado cambiará a "procesado" (verde) o "fallido" (rojo)
   - Aparecerá una notificación con el resultado
   - Todo sin recargar la página

### Prueba 2: Asistente de IA

1. **Scroll hasta "🤖 Asistente de Resumen con IA"**

2. **Haz clic en el botón "Python"** (texto de ejemplo)

3. **Haz clic en "✨ Generar Resumen"**

4. **Observa el resultado:**
   - Resumen generado (modo mock o real según tu configuración)
   - Modelo usado
   - Tokens consumidos
   - ID del resumen

### Prueba 3: RPA (Opcional)

**Abre una quinta terminal:**

```bash
cd rpa
source venv/bin/activate  # Windows: venv\Scripts\activate
python wikipedia_scraper.py
```

**Observa:**

- El script navega a Wikipedia
- Extrae el primer párrafo
- Toma un screenshot
- Envía al asistente de IA
- Muestra el resumen generado

**Resultados guardados en:**

- `rpa/screenshots/wikipedia_*.png`
- `rpa/screenshots/result_*.json`

---

### Documentación Adicional

- **README.md** - Visión general del proyecto
- **ARQUITECTURA.md** - Detalles técnicos y arquitectura

---
