from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from app.db.session import get_db
from sqlalchemy.orm import Session
from schemas.defects import DefectListOut, DefectCreate, DefectOut, DefectUpdate
from services.defects import list_defects, create_defect, get_defect, update_defect

router = APIRouter(prefix="/defects", tags=["defects"])

@router.get("", response_model=DefectListOut)
def get_defects(limit: int = 50, offset: int = 0, status: str = None, category: str = None, db: Session = Depends(get_db)):
    items, total = list_defects(db, limit, offset, status=status, category=category)
    return DefectListOut(items=items, limit=limit, offset=offset, total=total, status=status, category=category)

@router.post("", response_model=DefectOut, status_code=201)
def create_new_defect(defect_data: DefectCreate, db: Session = Depends(get_db)):
    new_defect = create_defect(db, defect_data.model_dump())
    return new_defect

@router.get("/{defect_id}", response_model=DefectOut)
def get_defect_by_id(defect_id: UUID, db: Session = Depends(get_db)):
    defect = get_defect(db, defect_id)
    if not defect:
        raise HTTPException(status_code=404, detail="Defect not found")
    return defect

@router.patch("/{defect_id}", response_model=DefectOut)
def update_defect_by_id(defect_id: UUID, update_data: DefectUpdate, db: Session = Depends(get_db)):
    updated_defect = update_defect(db, defect_id, update_data.model_dump(exclude_unset=True))
    if not updated_defect:
        raise HTTPException(status_code=404, detail="Defect not found")
    return updated_defect