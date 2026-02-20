from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.domains.enums import IncidentStatus
from app.domains.enums import IncidentSeverity

class SafetyIncidentCreate(BaseModel):
    severity: IncidentSeverity
    description: str | None = None
    location: str
    department: str
    shift: str

class SafetyIncidentUpdate(BaseModel):
    severity: IncidentSeverity | None = None
    description: str | None = None
    location: str | None = None
    department: str | None = None
    shift: str | None = None
    corrective_action: str | None = None

class SafetyIncidentOut(BaseModel):
    id: UUID
    severity: IncidentSeverity
    description: str | None
    location: str
    department: str
    shift: str
    status: IncidentStatus
    corrective_action: str | None
    reported_by: UUID
    created_at: datetime

    class Config:
        from_attributes=True


