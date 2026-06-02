from sqlalchemy.orm import Session
import models
import schemas


def get_products(db: Session):
    return db.query(models.Product).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_sku(db: Session, sku: str):
    return db.query(models.Product).filter(models.Product.sku == sku).first()

def create_product(db: Session, product: schemas.ProductCreate):
    db_obj = models.Product(**product.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    db_obj = get_product(db, product_id)
    for k, v in product.dict().items():
        setattr(db_obj, k, v)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_product(db: Session, product_id: int):
    db.query(models.Product).filter(models.Product.id == product_id).delete()
    db.commit()


def get_customers(db: Session):
    return db.query(models.Customer).all()

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customer_by_email(db: Session, email: str):
    return db.query(models.Customer).filter(models.Customer.email == email).first()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_obj = models.Customer(**customer.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_customer(db: Session, customer_id: int, customer: schemas.CustomerCreate):
    db_obj = get_customer(db, customer_id)
    for k, v in customer.dict().items():
        setattr(db_obj, k, v)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_customer(db: Session, customer_id: int):
    db.query(models.Customer).filter(models.Customer.id == customer_id).delete()
    db.commit()


def get_orders(db: Session):
    return db.query(models.Order).all()

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def create_order(db: Session, order: schemas.OrderCreate):
    total = 0.0
    db_order = models.Order(customer_id=order.customer_id, status="pending")
    db.add(db_order)
    db.flush()
    for item in order.items:
        product = get_product(db, item.product_id)
        total += product.price * item.quantity
        product.stock -= item.quantity
        db.add(models.OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=product.price,
        ))
    db_order.total_amount = total
    db.commit()
    db.refresh(db_order)
    return db_order
