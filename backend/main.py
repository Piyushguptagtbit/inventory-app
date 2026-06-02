from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
import crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    if crud.get_product_by_sku(db, product.sku):
        raise HTTPException(400, "SKU already exists")
    return crud.create_product(db, product)

@app.get("/products/{pid}", response_model=schemas.Product)
def get_product(pid: int, db: Session = Depends(get_db)):
    p = crud.get_product(db, pid)
    if not p:
        raise HTTPException(404, "Not found")
    return p

@app.put("/products/{pid}", response_model=schemas.Product)
def update_product(pid: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    if not crud.get_product(db, pid):
        raise HTTPException(404, "Not found")
    return crud.update_product(db, pid, product)

@app.delete("/products/{pid}")
def delete_product(pid: int, db: Session = Depends(get_db)):
    if not crud.get_product(db, pid):
        raise HTTPException(404, "Not found")
    crud.delete_product(db, pid)
    return {"message": "Deleted"}

@app.get("/customers", response_model=List[schemas.Customer])
def list_customers(db: Session = Depends(get_db)):
    return crud.get_customers(db)

@app.post("/customers", response_model=schemas.Customer, status_code=201)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    if crud.get_customer_by_email(db, customer.email):
        raise HTTPException(400, "Email already registered")
    return crud.create_customer(db, customer)

@app.get("/customers/{cid}", response_model=schemas.Customer)
def get_customer(cid: int, db: Session = Depends(get_db)):
    c = crud.get_customer(db, cid)
    if not c:
        raise HTTPException(404, "Not found")
    return c

@app.put("/customers/{cid}", response_model=schemas.Customer)
def update_customer(cid: int, customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    if not crud.get_customer(db, cid):
        raise HTTPException(404, "Not found")
    return crud.update_customer(db, cid, customer)

@app.delete("/customers/{cid}")
def delete_customer(cid: int, db: Session = Depends(get_db)):
    if not crud.get_customer(db, cid):
        raise HTTPException(404, "Not found")
    crud.delete_customer(db, cid)
    return {"message": "Deleted"}

@app.get("/orders", response_model=List[schemas.Order])
def list_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)

@app.post("/orders", response_model=schemas.Order, status_code=201)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    if not crud.get_customer(db, order.customer_id):
        raise HTTPException(404, "Customer not found")
    for item in order.items:
        p = crud.get_product(db, item.product_id)
        if not p:
            raise HTTPException(404, f"Product {item.product_id} not found")
        if p.stock < item.quantity:
            raise HTTPException(400, f"Insufficient stock for {p.item_name}")
    return crud.create_order(db, order)

@app.get("/orders/{oid}", response_model=schemas.Order)
def get_order(oid: int, db: Session = Depends(get_db)):
    o = crud.get_order(db, oid)
    if not o:
        raise HTTPException(404, "Not found")
    return o
