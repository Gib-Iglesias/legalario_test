from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database import get_db
from ..models import Transaction, TransactionStatus
from ..schemas import TransactionCreate, TransactionResponse, AsyncProcessRequest, AsyncProcessResponse
from ..tasks import process_transaction
import hashlib
import json

router = APIRouter(prefix="/transactions", tags=["transactions"])

def generate_idempotency_key(data: dict) -> str:
    """Genera una clave de idempotencia basada en el contenido"""
    content = json.dumps(data, sort_keys=True)
    return hashlib.sha256(content.encode()).hexdigest()

@router.post("/create", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    idempotency_key: Optional[str] = Header(None, alias="X-Idempotency-Key")
):
    """
    Crea una nueva transacción de forma idempotente.
    
    - **user_id**: ID del usuario que realiza la transacción
    - **monto**: Monto de la transacción (debe ser positivo)
    - **tipo**: Tipo de transacción (deposito, retiro, transferencia)
    
    La idempotencia se maneja mediante:
    1. Header X-Idempotency-Key (recomendado)
    2. Campo idempotency_key en el body
    3. Generación automática basada en el contenido
    """
    
    # Determinar la clave de idempotencia
    final_idempotency_key = (
        idempotency_key or 
        transaction.idempotency_key or 
        generate_idempotency_key({
            "user_id": transaction.user_id,
            "monto": transaction.monto,
            "tipo": transaction.tipo
        })
    )
    
    # Verificar si ya existe una transacción con esta clave
    existing_transaction = db.query(Transaction).filter(
        Transaction.idempotency_key == final_idempotency_key
    ).first()
    
    if existing_transaction:
        # Retornar la transacción existente (idempotencia)
        return existing_transaction
    
    # Crear nueva transacción
    db_transaction = Transaction(
        user_id=transaction.user_id,
        monto=transaction.monto,
        tipo=transaction.tipo,
        idempotency_key=final_idempotency_key
    )
    
    try:
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la transacción: {str(e)}"
        )


@router.post("/async-process", response_model=AsyncProcessResponse)
async def async_process_transaction(
    request: AsyncProcessRequest,
    db: Session = Depends(get_db)
):
    """
    Encola una transacción para procesamiento asíncrono.
    
    - **transaction_id**: ID de la transacción a procesar
    
    La transacción se procesa en background mediante Celery + Redis.
    El worker simula procesamiento con sleep y puede fallar aleatoriamente.
    """
    
    # Verificar que la transacción existe
    transaction = db.query(Transaction).filter(
        Transaction.id == request.transaction_id
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transacción {request.transaction_id} no encontrada"
        )
    
    # Verificar que no esté ya procesada
    if transaction.estado == TransactionStatus.PROCESADO.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La transacción ya fue procesada"
        )
    
    # Encolar la tarea
    task = process_transaction.delay(request.transaction_id)
    
    return AsyncProcessResponse(
        message="Transacción encolada para procesamiento",
        transaction_id=request.transaction_id,
        task_id=task.id,
        status="enqueued"
    )

@router.get("/list", response_model=List[TransactionResponse])
async def list_transactions(
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[str] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Lista todas las transacciones con filtros opcionales.
    
    - **skip**: Número de registros a saltar (paginación)
    - **limit**: Número máximo de registros a retornar
    - **user_id**: Filtrar por ID de usuario
    - **estado**: Filtrar por estado (pendiente, procesado, fallido)
    """
    query = db.query(Transaction)
    
    if user_id:
        query = query.filter(Transaction.user_id == user_id)
    
    if estado:
        query = query.filter(Transaction.estado == estado)
    
    transactions = query.offset(skip).limit(limit).all()
    return transactions

@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene una transacción específica por ID.
    """
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transacción {transaction_id} no encontrada"
        )
    
    return transaction


from fastapi import WebSocket, WebSocketDisconnect
from ..websocket_manager import manager
import asyncio

@router.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket, user_id: Optional[str] = None):
    """
    WebSocket para recibir notificaciones en tiempo real de cambios en transacciones.
    
    - **user_id**: (Opcional) ID de usuario para filtrar notificaciones
    
    Conecta al WebSocket y recibirás notificaciones cuando:
    - Se cree una nueva transacción
    - Una transacción cambie de estado (pendiente → procesado/fallido)
    
    Formato de mensaje:
    {
        "type": "transaction_update",
        "data": {...},  // Datos de la transacción
        "timestamp": "2024-01-01T00:00:00"
    }
    """
    await manager.connect(websocket, user_id)
    
    try:
        # Enviar mensaje de bienvenida
        await manager.send_personal_message({
            "type": "connection_established",
            "message": "Conectado al stream de transacciones",
            "user_id": user_id
        }, websocket)
        
        # Mantener la conexión abierta y escuchar mensajes del cliente
        while True:
            try:
                # Recibir mensajes del cliente (ping/pong para mantener conexión)
                data = await websocket.receive_text()
                
                # Responder a ping
                if data == "ping":
                    await manager.send_personal_message({
                        "type": "pong",
                        "timestamp": str(asyncio.get_event_loop().time())
                    }, websocket)
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                print(f"Error en WebSocket: {e}")
                break
    
    finally:
        manager.disconnect(websocket, user_id)

@router.get("/stats")
async def get_transaction_stats(db: Session = Depends(get_db)):
    """
    Obtiene estadísticas de las transacciones.
    """
    from sqlalchemy import func
    
    total = db.query(func.count(Transaction.id)).scalar()
    
    stats_by_status = db.query(
        Transaction.estado,
        func.count(Transaction.id)
    ).group_by(Transaction.estado).all()
    
    stats_by_type = db.query(
        Transaction.tipo,
        func.count(Transaction.id)
    ).group_by(Transaction.tipo).all()
    
    return {
        "total": total,
        "by_status": {status: count for status, count in stats_by_status},
        "by_type": {tipo: count for tipo, count in stats_by_type},
        "active_websocket_connections": len(manager.active_connections)
    }
