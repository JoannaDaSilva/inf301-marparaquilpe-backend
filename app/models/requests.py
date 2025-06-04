# app/models/request.py
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import date

class NewRequest(BaseModel):
    product_id: UUID
    user_id: UUID
    quantity: int = Field(..., gt=0)
    comment: Optional[str] = None
    product_item_id: Optional[UUID] = None

class RequestStatusUpdate(BaseModel):
    status: str  # Solo permitir: 'pending', 'approved', 'rejected'
