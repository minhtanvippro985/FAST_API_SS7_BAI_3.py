from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field


class BuyProduct(BaseModel):
    id :int #= Field(...,gt=0)
    buy_amount:int #= Field(...,gt=0)


app = FastAPI()

products_db = [
    {"id": 101, "name": "Bàn phím cơ", "stock": 5, "price": 1200000.0},
    {"id": 102, "name": "Chuột Gaming", "stock": 2, "price": 600000.0}
]
orders_db = []



@app.get("/products")
def display_products():
    return products_db

@app.post("/products")
def buy_product(buy_prod:BuyProduct):
    found = None
    for product in products_db:
        if product["id"] == buy_prod.id:
            found = product
            break
    if found is None:
        raise HTTPException(status_code=404 , detail = "Khong tim thay san pham")


    if buy_prod.buy_amount <= 0:
        raise HTTPException(status_code=400 , detail= "So hang mua phai lon hon 0")
    
 
    
    if buy_prod.buy_amount > found["stock"]:
        raise HTTPException(status_code=400 , detail="San pham khong du so luong")
    
    found["stock"] = found["stock"] - buy_prod.buy_amount
    new_order = {
        "order_id" : len(orders_db) +1 ,
        "product_id" : buy_prod.id,
        "amount" : buy_prod.buy_amount
    }
    orders_db.append(new_order)
    raise HTTPException(status_code=201 , detail="Da tao don hang moi")
    