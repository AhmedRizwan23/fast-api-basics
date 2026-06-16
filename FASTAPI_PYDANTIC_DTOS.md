# FastAPI Basics and Pydantic DTOs

This document summarizes the minimal, practical concepts used in this workspace: `FastAPI` for building APIs and `Pydantic` (v2) models as DTOs for request validation.

**Files**
- `main.py` — FastAPI application and endpoints.
- `dtos.py` — Pydantic DTO (`productDTO`) used to validate request bodies.
- `mockData.py` — In-memory `products` list used as mock persistence.

---

## Quick setup

1. Create and activate a virtual environment (already in this workspace):

```powershell
python -m venv env
env\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install fastapi uvicorn
```

(FastAPI will bring `pydantic` as a dependency; if you need explicit pydantic features, install `pydantic`.)

3. Run the app (from project root):

```bash
uvicorn main:app --reload --port 8000
```

Open `http://127.0.0.1:8000/docs` for interactive OpenAPI UI.

---

## Key FastAPI concepts used

- App instance: `app = FastAPI()` in `main.py`.
- Route decorators: `@app.get`, `@app.post`, `@app.put`, `@app.delete`.
- Path parameters: declare in path string and function signature, e.g. `/products/{product_id}` and `product_id: int`.
- Query parameters: function args not in path are treated as query params (or read via `Request`).
- Request body: declare a Pydantic model type in the function params to parse & validate JSON body.
- Response: return Python dicts / lists. For more control use `response_model` and HTTP status codes.

### Example endpoints in this project
- `GET /` — welcome message.
- `GET /products` and `GET /all_products` — return mock product list.
- `GET /products/{product_id}` and `GET /product/{product_id}` — path parameter lookups.
- `GET /greeting?name=Joe&age=30` — query params example.
- `GET /greet?name=Joe&age=30` — reading `request.query_params` manually.
- `POST /create_product` — creates a product using a `productDTO` body.
- `PUT /update_product/{product_id}` — updates a product using `productDTO`.
- `DELETE /delete_product/{product_id}` — deletes a product by id.

---

## Pydantic DTOs (in `dtos.py`)

- DTOs are Pydantic `BaseModel` classes used to validate and parse request JSON.
- Example from this repo:

```python
from pydantic import BaseModel

class productDTO(BaseModel):
    id: int
    title: str
    price: int = 0
    count: int = 0
```

- When you declare `product_data: productDTO` in an endpoint, FastAPI will:
  - Parse the incoming JSON into `productDTO`.
  - Validate types and required fields, returning a 422 response on errors.

- In Pydantic v2 use `product_data.model_dump()` to convert to a plain dict suitable for storing/sending.

---

## Example requests (curl)

List products:

```bash
curl http://127.0.0.1:8000/products
```

Get product by id:

```bash
curl http://127.0.0.1:8000/products/1
```

Create a product:

```bash
curl -X POST "http://127.0.0.1:8000/create_product" -H "Content-Type: application/json" -d '{"id":5,"title":"New Item","price":123,"count":2}'
```

Update a product:

```bash
curl -X PUT "http://127.0.0.1:8000/update_product/5" -H "Content-Type: application/json" -d '{"id":5,"title":"Updated Item","price":150,"count":3}'
```

Delete a product:

```bash
curl -X DELETE "http://127.0.0.1:8000/delete_product/5"
```

---

## Tips & next improvements

- Use `response_model=productDTO` on endpoints to document and validate responses.
- Return proper HTTP status codes and raise `HTTPException(status_code=404, detail="Not found")` for missing resources.
- Persist to a database instead of using the in-memory `products` list.
- Add tests using `httpx` and `pytest` to validate endpoints.
- Consider `router` modularization for larger apps (split routes to multiple files).

---

If you want, I can:
- Add `response_model` annotations to `main.py`.
- Add example Postman collection or more examples.
- Create a small README with run steps.

---

## Concept explanations

- `enumerate(iterable)`:
  - Returns pairs `(index, item)` while iterating. In `main.py` it's used in `update_product` to get the index of the matching item so the code can replace `products[index] = updated_dict` safely.
  - Why use it: it lets you update a list in-place by index while iterating, which is simpler and less error-prone than searching again for an index.

- `product_data.model_dump()` (Pydantic v2):
  - Pydantic model instances are not plain dictionaries; `.model_dump()` converts the validated model into a serializable Python `dict`.
  - Why use it: convert the model to a dict before appending to `products` or before sending it as JSON in responses.
  - Note: in Pydantic v1 the equivalent was `.dict()`.

- `request.query_params`:
  - FastAPI exposes request-level query params via the `Request` object as an immutable `MultiDict`-like mapping.
  - Converting to `dict(request.query_params)` yields a plain dict for easier access and logging.

- Why use DTOs / Pydantic models:
  - Validation: required fields and types are validated automatically; invalid requests return a 422 response.
  - Parsing: incoming JSON is parsed into typed Python objects, reducing manual parsing code.
  - Documentation: models automatically show in the OpenAPI schema and Swagger UI, improving API discoverability.

- Other small notes:
  - Use `enumerate` when you need an item's index during iteration; use simple `for item in list` when you only need the value.
  - When updating or deleting items, prefer identifying items by a unique id and returning appropriate HTTP status codes (e.g., 201 for created, 404 for not found).
  - When returning data to clients, consider `response_model` and `status_code` in the route decorator for clearer OpenAPI docs and stronger validation.

