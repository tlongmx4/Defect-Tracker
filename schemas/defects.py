from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List

from app.domains.enums import DefectStatus

class DefectCreate(BaseModel):
    reported_by: str
    category: str
    subcategory: Optional[str] = None
    description: Optional[str] = None
    absn: str
    assigned_to: Optional[str] = None
    status: DefectStatus

class DefectOut(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    reported_by: str
    category: str
    subcategory: Optional[str] = None
    description: Optional[str] = None
    absn: str
    assigned_to: Optional[str] = None
    status: DefectStatus

    model_config = ConfigDict(from_attributes=True)

class DefectListOut(BaseModel):
    items: List[DefectOut]
    limit: int
    offset: int
    status: Optional[str] = None
    category: Optional[str] = None
    total: int

    model_config = ConfigDict(from_attributes=True)

class DefectUpdate(BaseModel):
    category: Optional[str] = None
    subcategory: Optional[str] = None
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    status: Optional[DefectStatus] = None
