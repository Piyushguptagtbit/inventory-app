from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    sku: str
    description: Optional[str] = ""
    price: float
    stock: int = 0

class Product(ProductCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = ""
    address: Optional[str] = ""

class Customer(CustomerCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderItem(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemCreate]

class Order(BaseModel):
    id: int
    customer_id: int
    status: str
    total_amount: float
    created_at: datetime
    items: List[OrderItem] = []
    class Config:
        from_attributes = True
