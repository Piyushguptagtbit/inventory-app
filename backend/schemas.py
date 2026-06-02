from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ProductBase(BaseModel):
    sku: str
    description: Optional[str]
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    name: str
    created_at: datetime
    class Config:
        orm_mode = True


class CustomerBase(BaseModel):
    email: str
    phone: Optional[str]
    address: Optional[str]

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    name: str
    created_at: datetime
    class Config:
        orm_mode = True


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderItem(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    class Config:
        orm_mode = True

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
        orm_mode = True
