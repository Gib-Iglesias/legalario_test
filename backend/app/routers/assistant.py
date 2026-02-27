from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..database import get_db
from ..models import SummaryRequest as SummaryRequestModel
from ..schemas import SummarizeRequest, SummarizeResponse
from ..services.openai_service import OpenAIService
import os

router = APIRouter(prefix="/assistant", tags=["assistant"])

# Inicializar servicio de OpenAI
openai_service = OpenAIService(api_key=os.getenv("OPENAI_API_KEY"))


@router.post("/summarize", response_model=SummarizeResponse, status_code=status.HTTP_201_CREATED)
async def summarize_text(request: SummarizeRequest, db: Session = Depends(get_db)):
    """
    Genera un resumen de un texto usando la API de OpenAI.
    
    - **text**: Texto a resumir (mínimo 10 caracteres)
    
    El resumen se genera usando GPT-3.5-turbo o un mock si no hay API key.
    La petición y respuesta se registran en la base de datos.
    """
    
    # Crear registro en BD
    db_request = SummaryRequestModel(
        original_text=request.text,
        status="pending"
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    
    try:
        # Generar resumen con OpenAI
        result = await openai_service.summarize(request.text)
        
        # Actualizar registro con el resultado
        db_request.summary = result["summary"]
        db_request.model_used = result.get("model")
        db_request.tokens_used = result.get("tokens_used")
        db_request.status = "completed"
        db_request.completed_at = datetime.utcnow()
        
        db.commit()
        db.refresh(db_request)
        
        return db_request
        
    except Exception as e:
        # Registrar error
        db_request.status = "failed"
        db_request.error_message = str(e)
        db_request.completed_at = datetime.utcnow()
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar resumen: {str(e)}"
        )


@router.get("/summaries", response_model=List[SummarizeResponse])
async def list_summaries(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Lista todos los resúmenes generados.
    
    - **skip**: Número de registros a saltar (paginación)
    - **limit**: Número máximo de registros a retornar
    """
    summaries = db.query(SummaryRequestModel).order_by(
        SummaryRequestModel.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return summaries


@router.get("/summaries/{summary_id}", response_model=SummarizeResponse)
async def get_summary(summary_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un resumen específico por ID.
    """
    summary = db.query(SummaryRequestModel).filter(
        SummaryRequestModel.id == summary_id
    ).first()
    
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resumen {summary_id} no encontrado"
        )
    
    return summary


@router.get("/stats")
async def get_assistant_stats(db: Session = Depends(get_db)):
    """
    Obtiene estadísticas del asistente.
    """
    from sqlalchemy import func
    
    total = db.query(func.count(SummaryRequestModel.id)).scalar()
    
    stats_by_status = db.query(
        SummaryRequestModel.status,
        func.count(SummaryRequestModel.id)
    ).group_by(SummaryRequestModel.status).all()
    
    total_tokens = db.query(
        func.sum(SummaryRequestModel.tokens_used)
    ).scalar() or 0
    
    return {
        "total_requests": total,
        "by_status": {status: count for status, count in stats_by_status},
        "total_tokens_used": total_tokens
    }
