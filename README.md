# 📦 Monorepo de Proyectos Docker Compose

Este repositorio contiene 3 proyectos completos, autocontenidos y listos para producción o aprendizaje, combinando código fuente personalizado con imágenes oficiales listas para usar.

---

## 📁 Estructura del Monorepo

```plaintext
docker/
│
├── proyecto-1-web-stack/                  # Stack Web Clásico
│   ├── api/                               # Microservicio Node.js + Express
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── server.js
│   ├── frontend/                          # Nginx Web & Reverse Proxy
│   │   ├── index.html
│   │   └── nginx.conf
│   └── docker-compose.yaml                # PostgreSQL + Node.js + Nginx + Adminer
│
├── proyecto-2-async-processing/           # Sistema Asíncrono & Colas
│   ├── producer/                          # API FastAPI en Python
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── main.py
│   ├── worker/                            # Worker background en Python
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── worker.py
│   └── docker-compose.yaml                # Redis + FastAPI + Worker + Redis Commander
│
└── proyecto-3-microservices-observability/# Microservicios & Observabilidad
    ├── service-go/                        # Microservicio de alta velocidad en Go
    │   ├── Dockerfile
    │   └── main.go
    ├── prometheus.yml                     # Configuración de métricas
    └── docker-compose.yaml                # Go App + Prometheus + Grafana
```

---

## 🚀 Proyectos Incluidos

### 1️⃣ Proyecto 1: Web Stack (Node.js + PostgreSQL + Nginx + Adminer)

- **Propósito:** Aplicación CRUD de notas con arquitectura frontend/backend separada.
- **Servicios incluidos:**
  - `web` (`nginx:alpine`): Servidor web estático y reverse proxy en el puerto `8080`.
  - `api` (`Dockerfile` propio Node.js 20): API REST que se conecta a PostgreSQL.
  - `db` (`postgres:16-alpine`): Base de datos relacional con volumen persistente y healthcheck.
  - `db-admin` (`adminer:latest`): Gestor web de BD en el puerto `8081`.
- **Cómo ejecutar:**
  ```powershell
  cd .\proyecto-1-web-stack
  docker compose up --build -d
  ```

  - App web: [http://localhost:8080](http://localhost:8080)
  - Adminer: [http://localhost:8081](http://localhost:8081)

---

### 2️⃣ Proyecto 2: Procesamiento Asíncrono (FastAPI + Redis + Worker + Redis Commander)

- **Propósito:** Manejo de colas y tareas pesadas en segundo plano.
- **Servicios incluidos:**
  - `api-producer` (`Dockerfile` propio Python 3.11): FastAPI en puerto `8000` con interfaz web para encolar tareas.
  - `worker` (`Dockerfile` propio Python 3.11): Proceso en background que consume tareas con `BRPOP` de Redis y publica resultados.
  - `redis` (`redis:7-alpine`): Broker en memoria y base de datos de clave-valor.
  - `redis-ui` (`rediscommander/redis-commander`): UI web para inspeccionar colas y llaves en el puerto `8085`.
- **Cómo ejecutar:**
  ```powershell
  cd .\proyecto-2-async-processing
  docker compose up --build -d
  ```

  - Web UI / Encolar tareas: [http://localhost:8000](http://localhost:8000)
  - Redis Commander: [http://localhost:8085](http://localhost:8085)

---

### 3️⃣ Proyecto 3: Microservicios y Observabilidad (Go + Prometheus + Grafana)

- **Propósito:** Métricas, observabilidad y rendimiento con Go minimalista.
- **Servicios incluidos:**
  - `go-app` (`Dockerfile` multi-stage Go en Alpine): Microservicio ultraligero que expone `/health` y `/metrics` en puerto `8082`.
  - `prometheus` (`prom/prometheus:v2.50.0`): Scrapea métricas de la app cada 5 segundos en el puerto `9090`.
  - `grafana` (`grafana/grafana:10.3.3`): Plataforma de dashboards en puerto `3000` (User: `admin` / Password: `admin`).
- **Cómo ejecutar:**
  ```powershell
  cd .\proyecto-3-microservices-observability
  docker compose up --build -d
  ```

  - Go Microservice: [http://localhost:8082/health](http://localhost:8082/health)
  - Prometheus: [http://localhost:9090](http://localhost:9090)
  - Grafana: [http://localhost:3000](http://localhost:3000)
