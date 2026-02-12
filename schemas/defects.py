from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List

class DefectOut(BaseModel):
    id: UUID
    created_at: datetime
    reported_by: str
    category: str
    subcategory: Optional[str] = None
    description: Optional[str] = None
    absn: str
    assigned_to: Optional[str] = None
    status: str

    model_config = ConfigDict(from_attributes=True)

class DefectListOut(BaseModel):
    items: List[DefectOut]
    limit: int
    offset: int
    total: int

    model_config = ConfigDict(from_attributes=True)