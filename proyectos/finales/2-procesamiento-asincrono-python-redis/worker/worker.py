import os
import time
import json
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

def run_worker():
    print(f"Worker conectándose a Redis en {REDIS_HOST}:{REDIS_PORT}...")
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    while True:
        try:
            # brpop bloquea hasta recibir una tarea de la cola
            item = r.brpop("task_queue", timeout=5)
            if item:
                _, task_data = item
                task = json.loads(task_data)
                task_id = task.get("id")
                input_text = task.get("input", "")

                print(f"[Worker] Procesando tarea {task_id}: '{input_text}'")
                time.sleep(1.5) # Simula procesamiento intensivo de datos/IA

                result = {
                    "id": task_id,
                    "input": input_text,
                    "processed_result": f"TRANSFORMADO -> {input_text.upper()} (len: {len(input_text)})",
                    "processed_at": time.time()
                }

                # Guardar resultado en Redis con expiración de 1 hora
                r.setex(f"result:{task_id}", 3600, json.dumps(result))
                print(f"[Worker] Tarea {task_id} finalizada exitosamente.")
        except redis.ConnectionError:
            print("Esperando conexión con Redis...")
            time.sleep(2)
        except Exception as e:
            print(f"Error en worker: {e}")
            time.sleep(1)

if __name__ == "__main__":
    run_worker()
