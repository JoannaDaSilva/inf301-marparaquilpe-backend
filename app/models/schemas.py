from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserSignup(BaseModel):
    email: str
    password: str
    user_data: dict

class UserLogin(BaseModel):
    email: str
    password: str

class Product(BaseModel):
    id: str
    name: str
    description: Optional[str]
    is_individual: bool
    stock: int
    min_stock: Optional[int]
    created_at: datetime
    updated_at: datetime