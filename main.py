from fastapi import FastAPI ,Request
from mockData import products
from dtos import productDTO

app = FastAPI()

# creating our first endpoint
@app.get("/")
def home():
 return {"message": "welcome to fast api  !"}  

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


## path params
@app.get("/product/{product_id}")
def get_one_product(product_id : int):
    #if product avliable with the id ,return the product details else error message

    for oneProduct in products:
        if oneProduct.get("id")== product_id:
            return oneProduct

    return {"error" : "product not find for this id"}




# query params
@app.get("/greeting")
def greet_user( name : str , age :int):
    return {
        "greet" : f"hello {name} , your age is {age} ",
  },
    


# query params with request
@app.get("/greet")
def greet_user(request : Request):
    query_params=dict(request.query_params)
    print( f"query params are {query_params}")
    return {
        "greet" : f"hello  {query_params.get("name")} , your age is  {query_params.get("age")}",
  },


##body,headers-request headers,query params 
##diffrent types of http method
@app.post("/create_product")
def creeate_product(product_data : productDTO):
    print(f"data received from client {product_data}")
    product_data= product_data.model_dump()
    products.append(product_data)
    print(f"data received from client in model format {product_data}")
    return {"status" : "product created successfully ....." , "data is added to the list of products is" : products}



# to delete a product
@app.delete("/delete_product/{product_id}")
def delete_product(product_id : int):
    for product in products:
        if product.get("id") == product_id:
            products.remove(product)
            return {"status" : "product deleted successfully" , "data is" : products}
    return {"error" : "product not found for this id"}

#pydentic model - to validate the data

## how to validate data -Dtos
## hot to call diffrent http method -- any tool 