from pydantic import BaseModel


# Data Transfer Object (DTO) for products
# Uses Pydantic's BaseModel to validate incoming JSON payloads
class productDTO(BaseModel):
    # Unique numeric identifier for the product
    id: int
    # Human-readable product title/name
    title: str
    # Product price (default 0 if not provided)
    price: int = 0
    # Available item count/stock (default 0)
    count: int = 0





