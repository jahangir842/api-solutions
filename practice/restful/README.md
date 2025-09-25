## 🔹 RESTful API Lab Setup

### **1. Tools & Environment**

* **Backend Framework**: FastAPI (Python) – simple, modern, async-friendly.
* **Database**: SQLite (easy for testing, no setup needed).
* **HTTP Client**: `curl`, Postman, or Python `requests`.
* **Containerization**: Docker (optional, to practice deployment).
* **Reverse Proxy / Gateway**: Nginx or Kong (for advanced practice later).

---

### **2. Lab Directory Structure**

```bash
rest-api-lab/
├── app/
│   ├── main.py        # FastAPI app
│   ├── models.py      # Database models
│   ├── crud.py        # Database operations
│   ├── schemas.py     # Pydantic schemas
│   └── database.py    # DB connection
├── tests/
│   └── test_api.py    # pytest tests
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

### **3. Step 1: Create a Simple REST API (FastAPI)**

`app/main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to REST API Lab"}

# Example: GET with parameters
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}
```

Run it:

```bash
uvicorn app.main:app --reload
```

Test with curl:

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/items/5?q=hello
```

---

### **4. Step 2: Add CRUD Operations**

We’ll build an API for a simple **Todo app**:

* `POST /todos` → create a todo
* `GET /todos` → list all todos
* `GET /todos/{id}` → get a specific todo
* `PUT /todos/{id}` → update a todo
* `DELETE /todos/{id}` → delete a todo

---

### **5. Step 3: Test the API**

* Use **curl**:

  ```bash
  curl -X POST http://127.0.0.1:8000/todos -H "Content-Type: application/json" -d '{"title": "Learn REST", "completed": false}'
  curl http://127.0.0.1:8000/todos
  ```
* Or use **Postman / Insomnia**.

---

### **6. Step 4: Dockerize the API**

`Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### **7. Step 5: Advanced Practice**

* Add **authentication (JWT)**
* Add **rate limiting (Kong, Nginx, or FastAPI middleware)**
* Deploy to **Minikube** or **Docker Compose**
* Use **pytest** to automate API testing

---

