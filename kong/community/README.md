# Kong Community Edition with Docker Compose

A complete setup guide for running Kong Community Edition API Gateway using Docker Compose with PostgreSQL database.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Testing Your Setup](#testing-your-setup)
- [Basic Usage](#basic-usage)
- [Advanced Configuration](#advanced-configuration)
- [Plugin Management](#plugin-management)
- [Security & Authentication](#security--authentication)
- [Monitoring & Logging](#monitoring--logging)
- [Troubleshooting](#troubleshooting)
- [Production Considerations](#production-considerations)
- [API Reference](#api-reference)

## Overview

This setup provides:
- Kong Community Edition 3.6
- PostgreSQL 13 database
- Automatic database migrations
- Health checks for all services
- Persistent data storage
- Development and production-ready configuration

### Architecture
```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Client        │───▶│     Kong     │───▶│   Backend APIs  │
│                 │    │   Gateway    │    │                 │
└─────────────────┘    └──────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────┐
                       │ PostgreSQL   │
                       │   Database   │
                       └──────────────┘
```

## Prerequisites

- Docker (version 20.10+)
- Docker Compose (version 2.0+)
- curl (for testing)
- jq (optional, for JSON formatting)

### Installation on Ubuntu/Debian
```bash
# Install Docker
sudo apt update
sudo apt install docker.io docker-compose-plugin

# Add user to docker group (logout/login required)
sudo usermod -aG docker $USER

# Install jq for JSON formatting
sudo apt install jq
```

## Quick Start

### 1. Clone or Create Project Directory
```bash
mkdir kong-gateway
cd kong-gateway
```

### 2. Create docker-compose.yml
```yaml
services:
  kong-database:
    image: postgres:13
    container_name: kong-database
    environment:
      POSTGRES_USER: kong
      POSTGRES_DB: kong
      POSTGRES_PASSWORD: kongpass
    volumes:
      - kong_data:/var/lib/postgresql/data
    networks:
      - kong-net
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U kong"]
      interval: 30s
      timeout: 30s
      retries: 3

  kong-migrations:
    image: kong:3.6
    container_name: kong-migrations
    command: kong migrations bootstrap
    depends_on:
      kong-database:
        condition: service_healthy
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database
      KONG_PG_PORT: 5432
      KONG_PG_USER: kong
      KONG_PG_PASSWORD: kongpass
      KONG_PG_DATABASE: kong
    networks:
      - kong-net
    restart: "no"

  kong:
    image: kong:3.6
    container_name: kong-gateway
    depends_on:
      - kong-migrations
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database
      KONG_PG_PORT: 5432
      KONG_PG_USER: kong
      KONG_PG_PASSWORD: kongpass
      KONG_PG_DATABASE: kong
      KONG_PROXY_ACCESS_LOG: /dev/stdout
      KONG_ADMIN_ACCESS_LOG: /dev/stdout
      KONG_PROXY_ERROR_LOG: /dev/stderr
      KONG_ADMIN_ERROR_LOG: /dev/stderr
      KONG_ADMIN_LISTEN: 0.0.0.0:8001
      KONG_ADMIN_GUI_URL: http://localhost:8002
    networks:
      - kong-net
    ports:
      - "8000:8000"  # Proxy HTTP
      - "8001:8001"  # Admin API HTTP
      - "8443:8443"  # Proxy HTTPS
      - "8444:8444"  # Admin API HTTPS
    healthcheck:
      test: ["CMD", "kong", "health"]
      interval: 10s
      timeout: 10s
      retries: 10
    restart: unless-stopped

volumes:
  kong_data: {}

networks:
  kong-net:
    driver: bridge
```

### 3. Start the Services
```bash
sudo docker-compose up -d
```

### 4. Verify Installation
```bash
# Check containers are running
sudo docker ps

# Test Kong Admin API
curl -i http://localhost:8001/

# Check Kong status
curl -s http://localhost:8001/status | jq
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| KONG_DATABASE | Database type | postgres |
| KONG_PG_HOST | PostgreSQL host | kong-database |
| KONG_PG_PORT | PostgreSQL port | 5432 |
| KONG_PG_USER | Database user | kong |
| KONG_PG_PASSWORD | Database password | kongpass |
| KONG_PG_DATABASE | Database name | kong |
| KONG_ADMIN_LISTEN | Admin API listen address | 0.0.0.0:8001 |

### Port Mapping

| Port | Service | Protocol | Description |
|------|---------|----------|-------------|
| 8000 | Proxy | HTTP | Main gateway endpoint |
| 8001 | Admin API | HTTP | Management interface |
| 8443 | Proxy | HTTPS | Secure gateway endpoint |
| 8444 | Admin API | HTTPS | Secure management interface |

### Custom Configuration
Create a `.env` file for environment-specific variables:
```bash
# .env file
KONG_PG_PASSWORD=your_secure_password
KONG_ADMIN_GUI_URL=http://your-domain.com:8002
```

## Testing Your Setup

### Basic Health Check
```bash
# Kong health status
curl -s http://localhost:8001/status | jq

# Expected response:
{
  "database": {
    "reachable": true
  },
  "memory": {
    "workers_lua_vms": [
      {
        "http_allocated_gc": "0.02 MiB",
        "pid": 1
      }
    ]
  },
  "server": {
    "connections_accepted": 1,
    "connections_active": 1,
    "connections_handled": 1,
    "connections_reading": 0,
    "connections_waiting": 0,
    "connections_writing": 1,
    "total_requests": 1
  }
}
```

### Create Test Service and Route
```bash
# 1. Create a service pointing to httpbin.org
curl -X POST http://localhost:8001/services/ \
  --data "name=httpbin-service" \
  --data "url=http://httpbin.org"

# 2. Create a route for the service
curl -X POST http://localhost:8001/services/httpbin-service/routes \
  --data "hosts[]=api.local" \
  --data "paths[]=/api"

# 3. Test the proxy
curl -H "Host: api.local" http://localhost:8000/api/get
```

## Basic Usage

### Services Management

#### Create a Service
```bash
curl -X POST http://localhost:8001/services/ \
  --data "name=my-api" \
  --data "url=https://api.example.com"
```

#### List Services
```bash
curl -s http://localhost:8001/services | jq '.data[]'
```

#### Update a Service
```bash
curl -X PATCH http://localhost:8001/services/my-api \
  --data "url=https://new-api.example.com"
```

#### Delete a Service
```bash
curl -X DELETE http://localhost:8001/services/my-api
```

### Routes Management

#### Create a Route
```bash
curl -X POST http://localhost:8001/services/my-api/routes \
  --data "hosts[]=api.mycompany.com" \
  --data "paths[]=/v1" \
  --data "methods[]=GET" \
  --data "methods[]=POST"
```

#### List Routes
```bash
curl -s http://localhost:8001/routes | jq '.data[]'
```

#### Route with Multiple Conditions
```bash
curl -X POST http://localhost:8001/services/my-api/routes \
  --data "hosts[]=api.example.com" \
  --data "paths[]=/users" \
  --data "methods[]=GET" \
  --data "strip_path=true" \
  --data "preserve_host=false"
```

## Advanced Configuration

### SSL/TLS Configuration

#### Enable HTTPS for Admin API
Add to kong service environment:
```yaml
environment:
  # ... existing variables ...
  KONG_ADMIN_LISTEN: 0.0.0.0:8001, 0.0.0.0:8444 ssl
  KONG_SSL_CERT: /etc/ssl/certs/kong.crt
  KONG_SSL_CERT_KEY: /etc/ssl/certs/kong.key
volumes:
  - ./certs:/etc/ssl/certs
```

#### Create Self-Signed Certificates
```bash
mkdir certs
cd certs

# Generate private key
openssl genrsa -out kong.key 2048

# Generate certificate
openssl req -new -x509 -key kong.key -out kong.crt -days 365 \
  -subj "/C=US/ST=CA/L=SF/O=MyOrg/CN=localhost"
```

### Database Configuration

#### Custom PostgreSQL Settings
```yaml
kong-database:
  image: postgres:13
  environment:
    POSTGRES_USER: kong
    POSTGRES_DB: kong
    POSTGRES_PASSWORD: kongpass
    POSTGRES_INITDB_ARGS: "--auth-host=md5"
  command: >
    postgres
    -c max_connections=200
    -c shared_buffers=256MB
    -c effective_cache_size=1GB
```

### Performance Tuning

#### Kong Worker Configuration
```yaml
kong:
  environment:
    # ... existing variables ...
    KONG_NGINX_WORKER_PROCESSES: auto
    KONG_NGINX_WORKER_CONNECTIONS: 1024
    KONG_MEM_CACHE_SIZE: 128m
    KONG_PROXY_ACCESS_LOG: "off"  # Disable for performance
```

## Plugin Management

### Rate Limiting Plugin
```bash
# Apply to specific service
curl -X POST http://localhost:8001/services/my-api/plugins \
  --data "name=rate-limiting" \
  --data "config.minute=100" \
  --data "config.hour=10000"

# Apply globally
curl -X POST http://localhost:8001/plugins \
  --data "name=rate-limiting" \
  --data "config.minute=1000" \
  --data "config.hour=100000"
```

### CORS Plugin
```bash
curl -X POST http://localhost:8001/services/my-api/plugins \
  --data "name=cors" \
  --data "config.origins=*" \
  --data "config.methods=GET,POST,PUT,DELETE" \
  --data "config.headers=Accept,Authorization,Content-Type"
```

### Request/Response Transformation
```bash
# Add request header
curl -X POST http://localhost:8001/services/my-api/plugins \
  --data "name=request-transformer" \
  --data "config.add.headers=X-API-Version:v1"

# Add response header
curl -X POST http://localhost:8001/services/my-api/plugins \
  --data "name=response-transformer" \
  --data "config.add.headers=X-Powered-By:Kong"
```

### List Plugins
```bash
# List all installed plugins
curl -s http://localhost:8001/plugins | jq '.data[]'

# List available plugins
curl -s http://localhost:8001/plugins/enabled | jq
```

## Security & Authentication

### API Key Authentication
```bash
# Enable key-auth plugin
curl -X POST http://localhost:8001/services/my-api/plugins \
  --data "name=key-auth"

# Create consumer
curl -X POST http://localhost:8001/consumers/ \
  --data "username=john-doe"

# Create API key for consumer
curl -X POST http://localhost:8001/consumers/john-doe/key-auth \
  --data "key=my-secret-api-key"

# Test with API key
curl -H "apikey: my-secret-api-key" \
  http://localhost:8000/api/get
```

### Basic Authentication
```bash
# Enable basic-auth plugin
curl -X POST http://localhost:8001/services/my-api/plugins \
  --data "name=basic-auth"

# Create credentials for consumer
curl -X POST http://localhost:8001/consumers/john-doe/basic-auth \
  --data "username=john" \
  --data "password=secret123"

# Test with basic auth
curl -u john:secret123 http://localhost:8000/api/get
```

### JWT Authentication
```bash
# Enable JWT plugin
curl -X POST http://localhost:8001/services/my-api/plugins \
  --data "name=jwt"

# Create JWT credentials for consumer
curl -X POST http://localhost:8001/consumers/john-doe/jwt \
  --data "key=my-jwt-key" \
  --data "secret=my-jwt-secret"
```

### OAuth2 Plugin
```bash
# Enable OAuth2
curl -X POST http://localhost:8001/services/my-api/plugins \
  --data "name=oauth2" \
  --data "config.scopes=read,write" \
  --data "config.enable_authorization_code=true"

# Create OAuth2 application
curl -X POST http://localhost:8001/consumers/john-doe/oauth2 \
  --data "name=My App" \
  --data "client_id=my-client-id" \
  --data "client_secret=my-client-secret" \
  --data "redirect_uris[]=http://localhost:3000/callback"
```

## Monitoring & Logging

### Access Logs
Kong logs are configured to output to stdout/stderr. View them with:
```bash
# View Kong logs
sudo docker-compose logs kong

# Follow logs in real-time
sudo docker-compose logs -f kong

# View specific number of lines
sudo docker-compose logs --tail=100 kong
```

### Prometheus Metrics Plugin
```bash
# Enable Prometheus plugin
curl -X POST http://localhost:8001/plugins \
  --data "name=prometheus"

# Access metrics
curl http://localhost:8001/metrics
```

### File Logging Plugin
```bash
curl -X POST http://localhost:8001/services/my-api/plugins \
  --data "name=file-log" \
  --data "config.path=/tmp/kong-access.log"
```

### Request/Response Logging
```bash
# HTTP Log plugin
curl -X POST http://localhost:8001/services/my-api/plugins \
  --data "name=http-log" \
  --data "config.http_endpoint=http://localhost:3000/logs"

# TCP Log plugin
curl -X POST http://localhost:8001/services/my-api/plugins \
  --data "name=tcp-log" \
  --data "config.host=logserver.example.com" \
  --data "config.port=9999"
```

## Troubleshooting

### Common Issues and Solutions

#### Kong Container Keeps Restarting
```bash
# Check logs
sudo docker logs kong-gateway

# Common causes:
# 1. Database not ready - wait for migrations to complete
# 2. Database connection issues - check network connectivity
# 3. Configuration errors - verify environment variables
```

#### Database Connection Failed
```bash
# Check database container
sudo docker logs kong-database

# Test database connectivity
sudo docker exec -it kong-database psql -U kong -d kong -c "\l"

# Recreate with fresh database
sudo docker-compose down -v
sudo docker-compose up -d
```

#### Migration Issues
```bash
# Run migrations manually
sudo docker run --rm \
  --network kong-gateway_kong-net \
  -e "KONG_DATABASE=postgres" \
  -e "KONG_PG_HOST=kong-database" \
  -e "KONG_PG_USER=kong" \
  -e "KONG_PG_PASSWORD=kongpass" \
  -e "KONG_PG_DATABASE=kong" \
  kong:3.6 kong migrations bootstrap

# Check migration status
sudo docker run --rm \
  --network kong-gateway_kong-net \
  -e "KONG_DATABASE=postgres" \
  -e "KONG_PG_HOST=kong-database" \
  -e "KONG_PG_USER=kong" \
  -e "KONG_PG_PASSWORD=kongpass" \
  -e "KONG_PG_DATABASE=kong" \
  kong:3.6 kong migrations list
```

#### Port Conflicts
```bash
# Check if ports are in use
sudo netstat -tlnp | grep :8001

# Change ports in docker-compose.yml
ports:
  - "18000:8000"  # Use different host ports
  - "18001:8001"
```

### Health Check Commands
```bash
# Kong health
curl -f http://localhost:8001/status || echo "Kong is down"

# Database connectivity
sudo docker exec kong-gateway kong config db_connectivity

# Configuration validation
sudo docker exec kong-gateway kong config -c /etc/kong/kong.conf parse
```

### Performance Debugging
```bash
# Check Kong metrics
curl -s http://localhost:8001/status | jq '.server'

# Monitor resource usage
sudo docker stats kong-gateway kong-database

# Check slow queries (if enabled)
sudo docker exec kong-database psql -U kong -d kong \
  -c "SELECT query, mean_time FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;"
```

## Production Considerations

### Security Hardening

#### 1. Secure Admin API
```yaml
kong:
  environment:
    # Bind admin API to localhost only
    KONG_ADMIN_LISTEN: 127.0.0.1:8001
    # Or disable entirely and use declarative config
    KONG_ADMIN_LISTEN: "off"
```

#### 2. Use Strong Database Passwords
```yaml
kong-database:
  environment:
    POSTGRES_PASSWORD: "$(openssl rand -base64 32)"
```

#### 3. Enable SSL
```yaml
kong:
  environment:
    KONG_PROXY_LISTEN: 0.0.0.0:8000, 0.0.0.0:8443 ssl
    KONG_SSL_CERT: /etc/ssl/certs/kong.crt
    KONG_SSL_CERT_KEY: /etc/ssl/certs/kong.key
```

### High Availability Setup

#### Database Replication
```yaml
kong-database-replica:
  image: postgres:13
  environment:
    POSTGRES_USER: kong
    POSTGRES_DB: kong
    POSTGRES_PASSWORD: kongpass
    PGUSER: postgres
  command: |
    postgres
    -c wal_level=replica
    -c max_wal_senders=3
    -c max_replication_slots=3
```

#### Multiple Kong Instances
```yaml
kong-1:
  image: kong:3.6
  container_name: kong-gateway-1
  # ... configuration ...

kong-2:
  image: kong:3.6
  container_name: kong-gateway-2
  # ... configuration ...
```

#### Load Balancer (nginx)
```yaml
nginx-lb:
  image: nginx:alpine
  ports:
    - "80:80"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf
  depends_on:
    - kong-1
    - kong-2
```

### Backup and Recovery

#### Database Backup
```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
sudo docker exec kong-database pg_dump -U kong kong > "kong_backup_$DATE.sql"
gzip "kong_backup_$DATE.sql"
echo "Backup created: kong_backup_$DATE.sql.gz"
EOF

chmod +x backup.sh
```

#### Automated Backups
```yaml
kong-backup:
  image: postgres:13
  volumes:
    - ./backups:/backups
    - ./backup-script.sh:/backup-script.sh
  command: |
    sh -c '
    while true; do
      sleep 86400
      pg_dump -h kong-database -U kong kong > /backups/kong_backup_$(date +%Y%m%d_%H%M%S).sql
    done'
  depends_on:
    - kong-database
```

### Resource Limits
```yaml
kong:
  deploy:
    resources:
      limits:
        cpus: '2.0'
        memory: 2G
      reservations:
        cpus: '1.0'
        memory: 1G

kong-database:
  deploy:
    resources:
      limits:
        cpus: '1.0'
        memory: 1G
      reservations:
        cpus: '0.5'
        memory: 512M
```

## API Reference

### Admin API Endpoints

#### Services
- `GET /services` - List services
- `POST /services` - Create service
- `GET /services/{service}` - Get service
- `PATCH /services/{service}` - Update service
- `DELETE /services/{service}` - Delete service

#### Routes
- `GET /routes` - List routes
- `POST /routes` - Create route
- `GET /routes/{route}` - Get route
- `PATCH /routes/{route}` - Update route
- `DELETE /routes/{route}` - Delete route

#### Plugins
- `GET /plugins` - List plugins
- `POST /plugins` - Create plugin
- `GET /plugins/{plugin}` - Get plugin
- `PATCH /plugins/{plugin}` - Update plugin
- `DELETE /plugins/{plugin}` - Delete plugin

#### Consumers
- `GET /consumers` - List consumers
- `POST /consumers` - Create consumer
- `GET /consumers/{consumer}` - Get consumer
- `PATCH /consumers/{consumer}` - Update consumer
- `DELETE /consumers/{consumer}` - Delete consumer

### Useful Scripts

#### Check Kong Configuration
```bash
#!/bin/bash
echo "=== Kong Status ==="
curl -s http://localhost:8001/status | jq

echo -e "\n=== Services ==="
curl -s http://localhost:8001/services | jq '.data[] | {name, host, port}'

echo -e "\n=== Routes ==="
curl -s http://localhost:8001/routes | jq '.data[] | {hosts, paths, methods}'

echo -e "\n=== Plugins ==="
curl -s http://localhost:8001/plugins | jq '.data[] | {name, service, route}'
```

#### Kong Reset Script
```bash
#!/bin/bash
echo "Stopping Kong..."
sudo docker-compose down

echo "Removing volumes..."
sudo docker volume rm kong-gateway_kong_data

echo "Starting Kong..."
sudo docker-compose up -d

echo "Waiting for Kong to be ready..."
sleep 30

echo "Kong status:"
curl -s http://localhost:8001/status | jq '.database.reachable'
```

