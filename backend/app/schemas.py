from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class TransactionType(str, Enum):
    DEPOSITO = "deposito"
    RETIRO = "retiro"
    TRANSFERENCIA = "transferencia"

class TransactionStatus(str, Enum):
    PENDIENTE = "pendiente"
    PROCESADO = "procesado"
    FALLIDO = "fallido"

class TransactionCreate(BaseModel):
    user_id: str = Field(..., description="ID del usuario")
    monto: float = Field(..., gt=0, description="Monto de la transacción")
    tipo: TransactionType = Field(..., description="Tipo de transacción")
    idempotency_key: Optional[str] = Field(None, description="Clave para idempotencia")

class TransactionResponse(BaseModel):
    id: int
    user_id: str
    monto: float
    tipo: str
    estado: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class AsyncProcessRequest(BaseModel):
    transaction_id: int = Field(..., description="ID de la transacción a procesar")

class AsyncProcessResponse(BaseModel):
    message: str
    transaction_id: int
    task_id: str
    status: str


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Texto a resumir")


class SummarizeResponse(BaseModel):
    id: int
    original_text: str
    summary: str
    model_used: Optional[str] = None
    tokens_used: Optional[int] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
