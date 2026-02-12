from fastapi import APIRouter, Depends
from app.db.session import get_db
from sqlalchemy.orm import Session
from schemas.defects import DefectListOut
from services.defects import list_defects, create_defect

router = APIRouter(prefix="/defects", tags=["defects"])

@router.get("/defects", response_model=DefectListOut)
def get_defects(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    items, total = list_defects(db, limit, offset)
    return DefectListOut(items=items, limit=limit, offset=offset, total=total)