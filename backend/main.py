from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models, schemas, crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory & Order Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/products", response_model=List[schemas.Product])
def list_products(db: Session = Depends(get_db)):
    return crud.get_products(db)

@app.post("/products", response_model=schemas.Product, status_code=201)
def create_product(name: str, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    if crud.get_product_by_sku(db, product.sku):
        raise HTTPException(status_code=400, detail="SKU already exists")
    return crud.create_product(db, name, product)

@app.get("/products/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    p = crud.get_product(db, product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return p

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, name: str, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    p = crud.get_product(db, product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.update_product(db, product_id, name, product)

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    if not crud.get_product(db, product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    crud.delete_product(db, product_id)
    return {"message": "Deleted"}

@app.get("/customers", response_model=List[schemas.Customer])
def list_customers(db: Session = Depends(get_db)):
    return crud.get_customers(db)

@app.post("/customers", response_model=schemas.Customer, status_code=201)
def create_customer(name: str, customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    if crud.get_customer_by_email(db, customer.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_customer(db, name, customer)

@app.get("/customers/{customer_id}", response_model=schemas.Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    c = crud.get_customer(db, customer_id)
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    return c

@app.put("/customers/{customer_id}", response_model=schemas.Customer)
def update_customer(customer_id: int, name: str, customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    if not crud.get_customer(db, customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud.update_customer(db, customer_id, name, customer)

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    if not crud.get_customer(db, customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")
    crud.delete_customer(db, customer_id)
    return {"message": "Deleted"}

@app.get("/orders", response_model=List[schemas.Order])
def list_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)

@app.post("/orders", response_model=schemas.Order, status_code=201)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    if not crud.get_customer(db, order.customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")
    for item in order.items:
        p = crud.get_product(db, item.product_id)
        if not p:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if p.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {p.name}")
    return crud.create_order(db, order)

@app.get("/orders/{order_id}", response_model=schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    o = crud.get_order(db, order_id)
    if not o:
        raise HTTPException(status_code=404, detail="Order not found")
    return o
