Great choice 👍 Let’s start with **Kong API Gateway (Open Source)** using a **local Docker Compose lab**. This will give you a working setup quickly and let you understand the basics of routes, services, and plugins.

---

# 🏗 Lab 1: Kong with Docker Compose

### 📂 Folder Structure

```bash
api-management-labs/
└── kong/
    ├── docker-compose/
    │   ├── docker-compose.yml
    │   └── kong.yml
    └── labs.md
```

---

## 1️⃣ `docker-compose.yml`

This file runs **Kong Gateway** in **DB-less mode** (declarative config from YAML).

```yaml
version: "3.9"

services:
  kong:
    image: kong:3.5
    container_name: kong
    environment:
      KONG_DATABASE: "off"   # DB-less mode
      KONG_DECLARATIVE_CONFIG: /kong/declarative/kong.yml
      KONG_PROXY_LISTEN: 0.0.0.0:8000
      KONG_ADMIN_LISTEN: 0.0.0.0:8001
    volumes:
      - ./kong.yml:/kong/declarative/kong.yml:ro
    ports:
      - "8000:8000" # Proxy (for clients)
      - "8001:8001" # Admin API
```

---

## 2️⃣ `kong.yml`

Declarative config for Kong — we’ll expose a **mock service**.

```yaml
_format_version: "3.0"

services:
  - name: mock-service
    url: https://httpbin.org
    routes:
      - name: mock-route
        paths:
          - /httpbin
```

This means:

* Any request to `http://localhost:8000/httpbin/...` will be **proxied to `https://httpbin.org/...`**

Example:

```bash
curl http://localhost:8000/httpbin/get
```

➡ You’ll get a JSON response from **httpbin.org/get**.

---

## 3️⃣ Run the Lab

```bash
cd kong/docker-compose
docker-compose up -d
```

Check logs:

```bash
docker logs kong
```

Test route:

```bash
curl http://localhost:8000/httpbin/ip
```

---

## 4️⃣ Add a Plugin (Rate Limiting)

Update `kong.yml`:

```yaml
_format_version: "3.0"

services:
  - name: mock-service
    url: https://httpbin.org
    routes:
      - name: mock-route
        paths:
          - /httpbin

plugins:
  - name: rate-limiting
    service: mock-service
    config:
      minute: 5
      policy: local
```

Now restart:

```bash
docker-compose down
docker-compose up -d
```

Test by making **>5 requests/minute**:

```bash
for i in {1..10}; do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/httpbin/get; done
```

You’ll see some responses return **429 Too Many Requests** 🚫.

---

## 5️⃣ `labs.md` (Step-by-step Guide)

````markdown
# Kong API Gateway – Docker Compose Lab

## Objectives
- Run Kong in DB-less mode
- Expose a backend service
- Apply rate-limiting plugin

## Steps
1. Start Kong:
   ```bash
   docker-compose up -d
````

2. Verify service routing:

   ```bash
   curl http://localhost:8000/httpbin/ip
   ```
3. Enable rate-limiting plugin and reload Kong.
4. Test throttling with multiple requests.

## Next Steps

* Try adding `key-auth` plugin.
* Secure routes with JWT.
* Expose multiple services (users, orders, payments).



---

✅ With this, you now have a **working Kong API Gateway lab**.  
Next, we can extend it with:  
- **Key Authentication (API keys)**  
- **JWT Authentication**  
- **Prometheus metrics & Grafana dashboard**  

---

# 🔑 Lab 2: Kong with Key Authentication (API Key)

### 📂 Folder Structure (extended)

```bash
api-management-labs/
└── kong/
    ├── docker-compose/
    │   ├── docker-compose.yml
    │   ├── kong.yml
    │   └── consumers.yml   # API consumer definitions
    └── labs.md
```

---

## 1️⃣ Update `kong.yml`

We enable the **key-auth plugin** for the service:

```yaml
_format_version: "3.0"

services:
  - name: mock-service
    url: https://httpbin.org
    routes:
      - name: mock-route
        paths:
          - /httpbin

plugins:
  - name: key-auth
    service: mock-service
```

---

## 2️⃣ Create `consumers.yml`

Consumers represent **API clients** that will access your APIs.

```yaml
consumers:
  - username: dev-user
    keyauth_credentials:
      - key: my-secret-key-123
```

Now Kong knows about:

* A consumer: `dev-user`
* An API key: `my-secret-key-123`

---

## 3️⃣ Update `docker-compose.yml`

Mount both config files into Kong:

```yaml
version: "3.9"

services:
  kong:
    image: kong:3.5
    container_name: kong
    environment:
      KONG_DATABASE: "off"
      KONG_DECLARATIVE_CONFIG: /kong/declarative/kong.yml,/kong/declarative/consumers.yml
      KONG_PROXY_LISTEN: 0.0.0.0:8000
      KONG_ADMIN_LISTEN: 0.0.0.0:8001
    volumes:
      - ./kong.yml:/kong/declarative/kong.yml:ro
      - ./consumers.yml:/kong/declarative/consumers.yml:ro
    ports:
      - "8000:8000"
      - "8001:8001"
```

---

## 4️⃣ Run the Lab

```bash
cd kong/docker-compose
docker-compose down
docker-compose up -d
```

Test **without API key** (should fail with `401 Unauthorized`):

```bash
curl -i http://localhost:8000/httpbin/ip
```

Test **with API key**:

```bash
curl -i http://localhost:8000/httpbin/ip \
  --header "apikey: my-secret-key-123"
```

✅ Response should succeed.

---

## 5️⃣ `labs.md` (extend)

```markdown
# Lab 2: Kong with Key Authentication

## Objectives
- Secure API routes with API keys
- Create a consumer and assign keys
- Validate access control

## Steps
1. Enable the `key-auth` plugin in `kong.yml`.
2. Define consumers and credentials in `consumers.yml`.
3. Restart Kong with Docker Compose.
4. Test requests:
   - Without API key → `401 Unauthorized`
   - With API key → success

## Next Steps
- Add multiple consumers with different keys.
- Combine with rate-limiting plugin for per-consumer quotas.
- Try JWT authentication plugin.
```

---

👉 Do you want me to move next into **JWT Authentication** (so APIs require signed tokens), or should we first add **Prometheus monitoring + Grafana dashboard for Kong**?
