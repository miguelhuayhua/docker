import os
import json
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import redis

app = FastAPI(title="Async Task Producer")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
      <title>Proyecto 2 - Procesamiento Asíncrono</title>
      <style>
        body { font-family: sans-serif; max-width: 650px; margin: 40px auto; background: #0f172a; color: #f8fafc; }
        .card { background: #1e293b; padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #334155; }
        button { background: #38bdf8; border: none; padding: 10px 18px; border-radius: 4px; font-weight: bold; cursor: pointer; color: #0f172a; }
        input { padding: 10px; width: 60%; border-radius: 4px; border: 1px solid #475569; background: #0f172a; color: white; }
        ul { list-style: none; padding: 0; }
        li { background: #334155; margin: 5px 0; padding: 10px; border-radius: 4px; display: flex; justify-content: space-between; }
        .badge { background: #22c55e; color: black; padding: 2px 6px; border-radius: 4px; font-size: 12px; }
      </style>
    </head>
    <body>
      <h2>⚡ Sistema Asíncrono con Python, Redis y Celery/Worker</h2>
      <div class="card">
        <h3>Encolar Trabajo</h3>
        <input id="payload" placeholder="Texto o dato a procesar..." value="Tarea de ejemplo #1" />
        <button onclick="createTask()">Enviar a Cola Redis</button>
      </div>
      <div class="card">
        <h3>Trabajos Completados en Redis</h3>
        <button onclick="loadResults()">Actualizar Resultados</button>
        <ul id="results">Cargando...</ul>
      </div>

      <script>
        async function createTask() {
          const val = document.getElementById('payload').value;
          await fetch('/tasks', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ data: val })
          });
          alert('¡Tarea encolada en Redis!');
          setTimeout(loadResults, 1500);
        }

        async function loadResults() {
          const res = await fetch('/tasks');
          const data = await res.json();
          const list = document.getElementById('results');
          list.innerHTML = '';
          if (data.length === 0) {
            list.innerHTML = '<li>Sin resultados procesados aún.</li>';
            return;
          }
          data.forEach(item => {
            const li = document.createElement('li');
            li.innerHTML = `<span><b>[${item.id.substring(0,8)}]</b> ${item.input} &rarr; <i>${item.processed_result}</i></span> <span class="badge">PROCESADO</span>`;
            list.appendChild(li);
          });
        }
        loadResults();
        setInterval(loadResults, 4000);
      </script>
    </body>
    </html>
    """

@app.post("/tasks")
def enqueue_task(payload: dict):
    task_id = str(uuid.uuid4())
    job = {
        "id": task_id,
        "input": payload.get("data", "Default task")
    }
    r.lpush("task_queue", json.dumps(job))
    return {"status": "enqueued", "task_id": task_id}

@app.get("/tasks")
def list_completed_tasks():
    keys = r.keys("result:*")
    results = []
    for k in keys:
        val = r.get(k)
        if val:
            results.append(json.loads(val))
    return results
