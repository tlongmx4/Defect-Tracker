from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from services.safety_incidents import create_incident
from app.db.models import User
from app.core.auth import get_current_user
from schemas.safety import SafetyIncidentCreate

router = APIRouter(prefix="/api/safety/incidents", tags=["Safety"])

@router.post("")
def create_safety_incident(payload: SafetyIncidentCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        incident = create_incident(db, payload.dict(), current_user)
        return incident
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
