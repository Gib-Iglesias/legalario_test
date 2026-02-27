from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..websocket_manager import manager

router = APIRouter(prefix="/internal", tags=["internal"], include_in_schema=False)

class TransactionNotification(BaseModel):
    id: int
    user_id: str
    monto: float
    tipo: str
    estado: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

@router.post("/notify-transaction")
async def notify_transaction(notification: TransactionNotification, background_tasks: BackgroundTasks):
    """
    Endpoint interno para recibir notificaciones de cambios en transacciones.
    Usado por el worker de Celery para notificar a los clientes WebSocket.
    """
    transaction_data = notification.dict()
    
    # Notificar a todos los clientes conectados
    background_tasks.add_task(manager.notify_transaction_change, transaction_data)
    
    # También notificar específicamente al usuario
    background_tasks.add_task(manager.notify_transaction_to_user, notification.user_id, transaction_data)
    
    return {"status": "notified"}
