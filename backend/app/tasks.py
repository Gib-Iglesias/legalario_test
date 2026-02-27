from .celery_app import celery_app
from .database import SessionLocal
from .models import Transaction, TransactionStatus
import time
import random
import asyncio
import requests
import os

@celery_app.task(bind=True, name="process_transaction")
def process_transaction(self, transaction_id: int):
    """
    Procesa una transacción de forma asíncrona.
    Simula procesamiento con sleep y puede fallar aleatoriamente.
    """
    db = SessionLocal()
    
    try:
        # Obtener la transacción
        transaction = db.query(Transaction).filter(
            Transaction.id == transaction_id
        ).first()
        
        if not transaction:
            return {"status": "error", "message": "Transacción no encontrada"}
        
        # Actualizar estado a procesando (ya está en PENDIENTE por defecto)
        # Notificar inicio de procesamiento
        _notify_transaction_change(transaction)
        
        # Simular procesamiento (2-5 segundos)
        processing_time = random.uniform(2, 5)
        time.sleep(processing_time)
        
        # Simular posible fallo (10% de probabilidad)
        if random.random() < 0.1:
            transaction.estado = TransactionStatus.FALLIDO.value
            db.commit()
            db.refresh(transaction)
            
            # Notificar fallo
            _notify_transaction_change(transaction)
            
            return {
                "status": "failed",
                "transaction_id": transaction_id,
                "message": "Procesamiento fallido (simulado)"
            }
        
        # Procesamiento exitoso
        transaction.estado = TransactionStatus.PROCESADO.value
        db.commit()
        db.refresh(transaction)
        
        # Notificar éxito
        _notify_transaction_change(transaction)
        
        return {
            "status": "success",
            "transaction_id": transaction_id,
            "processing_time": round(processing_time, 2)
        }
        
    except Exception as e:
        # En caso de error, marcar como fallido
        if transaction:
            transaction.estado = TransactionStatus.FALLIDO.value
            db.commit()
        
        return {
            "status": "error",
            "transaction_id": transaction_id,
            "message": str(e)
        }
    
    finally:
        db.close()


def _notify_transaction_change(transaction: Transaction):
    """
    Notifica cambios en una transacción mediante HTTP POST al endpoint interno.
    Esto permite que el WebSocket manager reciba las actualizaciones.
    """
    try:
        # URL del servidor (ajustar según configuración)
        api_url = os.getenv("API_URL", "http://localhost:8000")
        
        # Preparar datos de la transacción
        transaction_data = {
            "id": transaction.id,
            "user_id": transaction.user_id,
            "monto": transaction.monto,
            "tipo": transaction.tipo,
            "estado": transaction.estado,
            "created_at": transaction.created_at.isoformat() if transaction.created_at else None,
            "updated_at": transaction.updated_at.isoformat() if transaction.updated_at else None
        }
        
        # Enviar notificación al endpoint interno (no bloqueante)
        requests.post(
            f"{api_url}/internal/notify-transaction",
            json=transaction_data,
            timeout=1
        )
    except Exception as e:
        # No fallar el procesamiento si la notificación falla
        print(f"Error notificando cambio de transacción: {e}")
