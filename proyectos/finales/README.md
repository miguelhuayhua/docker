# 🚀 Monorepo: Proyectos Finales en Docker Compose

Todos los proyectos se encuentran organizados dentro del directorio:
📂 `proyectos/finales/`

Cada proyecto es autocontenido, cuenta con su propio archivo `docker-compose.yaml`, su código fuente y servicios auxiliares con imágenes oficiales listas para usar.

---

## 📁 Estructura del Directorio `proyectos/finales/`

```plaintext
proyectos/
└── finales/
    │
    ├── 1-sistema-web-nodejs-postgres/
    │   ├── api/                               # Código backend (Express + PostgreSQL)
    │   │   ├── Dockerfile
    │   │   ├── package.json
    │   │   └── server.js
    │   ├── frontend/                          # Web SPA + Config Nginx
    │   │   ├── index.html
    │   │   └── nginx.conf
    │   └── docker-compose.yaml                # Nginx (8080) + Node API + Postgres + Adminer (8081)
    │
    ├── 2-procesamiento-asincrono-python-redis/
    │   ├── producer/                          # API FastAPI con UI interactiva para encolar
    │   │   ├── Dockerfile
    │   │   ├── requirements.txt
    │   │   └── main.py
    │   ├── worker/                            # Worker consumidor en segundo plano
    │   │   ├── Dockerfile
    │   │   ├── requirements.txt
    │   │   └── worker.py
    │   └── docker-compose.yaml                # FastAPI (8000) + Redis + Worker + Redis Commander (8085)
    │
    └── 3-microservicios-metricas-go-prometheus/
        ├── service-go/                        # Microservicio ultraligero en Go
        │   ├── Dockerfile
        │   └── main.go
        ├── prometheus.yml                     # Configuración de métricas
        └── docker-compose.yaml                # Go App (8082) + Prometheus (9090) + Grafana (3000)
```

---

## 🛠️ Detalle de Proyectos y Cómo Levantarlos

### 1️⃣ Proyecto 1: `1-sistema-web-nodejs-postgres`
- **Descripción:** Sistema web completo con base de datos relacional persistente y panel de administración visual.
- **Servicios incluidos:**
  - `web` (`nginx:alpine` en `http://localhost:8080`)
  - `api` (Node.js Express + pg)
  - `db` (`postgres:16-alpine` con healthcheck y volumen)
  - `db-admin` (`adminer:latest` en `http://localhost:8081`)
- **Comando para levantar:**
  ```powershell
  cd .\proyectos\finales\1-sistema-web-nodejs-postgres
  docker compose up --build -d
  ```

---

### 2️⃣ Proyecto 2: `2-procesamiento-asincrono-python-redis`
- **Descripción:** Arquitectura productora/consumidora para tareas pesadas en background usando colas Redis y visualizador gráfico.
- **Servicios incluidos:**
  - `api-producer` (FastAPI en `http://localhost:8000`)
  - `worker` (Script Python en background que procesa con `BRPOP`)
  - `redis` (`redis:7-alpine`)
  - `redis-ui` (`rediscommander/redis-commander` en `http://localhost:8085`)
- **Comando para levantar:**
  ```powershell
  cd .\proyectos\finales\2-procesamiento-asincrono-python-redis
  docker compose up --build -d
  ```

---

### 3️⃣ Proyecto 3: `3-microservicios-metricas-go-prometheus`
- **Descripción:** Microservicio de alto rendimiento con observabilidad nativa, monitoreo y tableros.
- **Servicios incluidos:**
  - `go-app` (Go nativo compilado en contenedor multi-stage en `http://localhost:8082/health` y `/metrics`)
  - `prometheus` (`prom/prometheus:v2.50.0` en `http://localhost:9090`)
  - `grafana` (`grafana/grafana:10.3.3` en `http://localhost:3000`, credenciales `admin`/`admin`)
- **Comando para levantar:**
  ```powershell
  cd .\proyectos\finales\3-microservicios-metricas-go-prometheus
  docker compose up --build -d
  ```
