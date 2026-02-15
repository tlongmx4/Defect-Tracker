from sqlalchemy import Column, Text, DateTime
from app.db.base import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid


class Defect(Base):
    __tablename__ = 'defects'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    reported_by = Column(Text, nullable=False)
    category = Column(Text, nullable=False)
    subcategory = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    absn = Column(Text, nullable=False)
    assigned_to = Column(Text, nullable=True)
    status = Column(Text, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by = Column(Text, nullable=True)

class DefectAuditLog(Base):
    __tablename__ = 'defect_audit_log'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    defect_id = Column(UUID(as_uuid=True), foreign_key='defects.id', nullable=False)
    changed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    changed_by = Column(Text, nullable=False)
    old_status = Column(Text, nullable=False)
    new_status = Column(Text, nullable=False)

