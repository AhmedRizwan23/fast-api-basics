from fastapi import FastAPI ,Request
from mockData import products
from dtos import productDTO

app = FastAPI()

# creating our first endpoint
from fastapi import FastAPI, Request
from mockData import products
from dtos import productDTO


# Create the FastAPI application instance
app = FastAPI()


# --- Basic routes ------------------------------------------------------

# Root endpoint: simple health/welcome message
@app.get("/")
def home():
    return {"message": "welcome to fast api  !"}


# Return the in-memory list of products (mock data)
@app.get("/products")
def get_products():
    return products


# Path parameter example: get a product by its numeric id
@app.get("/products/{product_id}")
def get_product(product_id: int):
    # Iterate the product list and return the matching item
    for product in products:
        if product["id"] == product_id:
            return product
    # If no product found, return a simple error message
    return {"message": "product not found"}


# Another example of a path parameter endpoint (same idea, different path)
@app.get("/product/{product_id}")
def get_one_product(product_id: int):
    # Search for the product with the provided id and return it
    for oneProduct in products:
        if oneProduct.get("id") == product_id:
            return oneProduct

    # Not found: return a JSON error
    return {"error": "product not find for this id"}



# --- Query parameters --------------------------------------------------

# Query parameters are declared as function args and validated by FastAPI
@app.get("/greeting")
def greet_user(name: str, age: int):
    # Returns a greeting using the provided query params, e.g. /greeting?name=Joe&age=30
    return {"greet": f"hello {name} , your age is {age} "}


# You can also read raw query parameters from the Request object
@app.get("/greet")
def greet_user_request(request: Request):
    # Convert the immutable query params to a plain dict for easier use
    query_params = dict(request.query_params)
    print(f"query params are {query_params}")
    # Use single quotes inside the f-string to avoid quoting conflicts
    return {
        "greet": f"hello  {query_params.get('name')} , your age is  {query_params.get('age')}"
    }



# --- Body, DTOs and HTTP methods --------------------------------------

# Create a product using a Pydantic/DTO model to validate the request body
@app.post("/create_product")
def create_product(product_data: productDTO):
    # `product_data` is a pydantic model; log and convert to dict
    print(f"data received from client {product_data}")
    product_dict = product_data.model_dump()
    # Append to the in-memory list (mock persistence)
    products.append(product_dict)
    print(f"data received from client in model format {product_dict}")
    return {"status": "product created successfully", "data": products}


# Return all products (alias of /products in this example)
@app.get("/all_products")
def get_all_products():
    return products


# Delete a product by id
@app.delete("/delete_product/{product_id}")
def delete_product(product_id: int):
    for product in products:
        if product.get("id") == product_id:
            products.remove(product)
            return {"status": "product deleted successfully", "data": products}
    return {"error": "product not found for this id"}


# Update a product by id using the DTO for validation
@app.put("/update_product/{product_id}")
def update_product(product_id: int, product_data: productDTO):
    for index, oneproduct in enumerate(products):
        if oneproduct.get("id") == product_id:
            product_dict = product_data.model_dump()
            products[index] = product_dict
            return {"status": "product updated successfully", "data": products}
    return {"error": "product not found for this id"}


# Notes for future work:
# - `productDTO` is used to validate incoming JSON bodies (Pydantic model)
# - Demonstrates path params, query params, request object, and body parsing
# - Consider adding proper HTTP status codes and exception handling for production