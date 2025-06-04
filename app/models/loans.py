
from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import date

class LoanCreate(BaseModel):
    request_id: UUID4
    due_date: date

class LoanUpdate(BaseModel):
    due_date: Optional[date] = None
    status: Optional[str] = None
