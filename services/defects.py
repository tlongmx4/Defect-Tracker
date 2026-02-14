from uuid import UUID
from app.db.models import Defect
from sqlalchemy.orm import Session

def list_defects(db: Session, limit: int, offset: int, status: str = None, category: str = None):
    base_query = db.query(Defect)
    if status is not None:
        base_query = base_query.filter(Defect.status == status)
    if category is not None:
        base_query = base_query.filter(Defect.category == category)
    total = base_query.count()
    items = base_query.order_by(Defect.created_at.desc()).offset(offset).limit(limit).all()
    return items, total
    

def create_defect(db: Session, defect_data: dict) -> Defect:
    new_defect = Defect(
        reported_by=defect_data['reported_by'],
        category=defect_data['category'],
        subcategory=defect_data.get('subcategory'),
        description=defect_data.get('description'),
        absn=defect_data['absn'],
        assigned_to=defect_data.get('assigned_to'),
        status=defect_data['status']
    )
    db.add(new_defect)
    db.commit()
    db.refresh(new_defect)
    return new_defect

def get_defect(db: Session, defect_id: UUID) -> Defect:
    return db.query(Defect).filter(Defect.id == defect_id).first()

def update_defect(db: Session, defect_id: UUID, update_data: dict) -> Defect:
    defect = db.query(Defect).filter(Defect.id == defect_id).first()
    if not defect:
        return None
    
    for key, value in update_data.items():
        if value is not None:
            setattr(defect, key, value)
    
    db.commit()
    db.refresh(defect)
    return defect
