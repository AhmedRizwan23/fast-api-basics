from fastapi import FastAPI
from mockData import products

app = FastAPI()

# creating our first endpoint
@app.get("/")
def home():
 return {"message": "welcome to fast api series !"}  

@app.get("/products")
def get_products():
    return products


#pass the id of the product to get the product details
@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    return {"message": "product not found"}