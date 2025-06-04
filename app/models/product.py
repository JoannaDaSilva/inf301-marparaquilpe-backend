from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Product(BaseModel):
    id: str
    name: str
    description: Optional[str]
    is_individual: bool
    stock: int
    min_stock: Optional[int]
    created_at: datetime
    updated_at: datetime

class NewProduct(BaseModel):
    name: str
    description: Optional[str]
    is_individual: bool
    stock: int
    min_stock: Optional[int]


class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    is_individual: Optional[bool]
    stock: Optional[int]
    min_stock: Optional[int]
