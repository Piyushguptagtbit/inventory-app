from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ProductCreate(BaseModel):
    item_name: str = ""
    sku: str = ""
    description: str = ""
    price: float = 0.0
    stock: int = 0

    class Config:
        orm_mode = True


class Product(BaseModel):
    id: int
    item_name: str
    sku: str
    description: str
    price: float
    stock: int
    created_at: datetime

    class Config:
        orm_mode = True


class CustomerCreate(BaseModel):
    customer_name: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""

    class Config:
        orm_mode = True


class Customer(BaseModel):
    id: int
    customer_name: str
    email: str
    phone: str
    address: str
    created_at: datetime

    class Config:
        orm_mode = True


class OrderItemCreate(BaseModel):
    product_id: int = 0
    quantity: int = 1

    class Config:
        orm_mode = True


class OrderItem(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float

    class Config:
        orm_mode = True


class OrderCreate(BaseModel):
    customer_id: int = 0
    items: List[OrderItemCreate] = []

    class Config:
        orm_mode = True


class Order(BaseModel):
    id: int
    customer_id: int
    status: str
    total_amount: float
    created_at: datetime
    items: List[OrderItem] = []

    class Config:
        orm_mode = True
