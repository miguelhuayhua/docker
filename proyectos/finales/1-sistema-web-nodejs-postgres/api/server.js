const express = require('express');
const { Pool } = require('pg');

const app = express();
const port = process.env.PORT || 3000;

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgres://appuser:appsecret123@db:5432/appdb'
});

app.use(express.json());

// Inicializar tabla si no existe
async function initDb() {
  let retries = 5;
  while (retries) {
    try {
      await pool.query(`
        CREATE TABLE IF NOT EXISTS notes (
          id SERIAL PRIMARY KEY,
          title VARCHAR(100) NOT NULL,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
      `);
      console.log('Base de datos conectada y tabla lista.');
      break;
    } catch (err) {
      console.log('Esperando a la base de datos... reintentos restantes:', retries);
      retries -= 1;
      await new Promise(res => setTimeout(res, 3000));
    }
  }
}
initDb();

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', service: 'Node.js Express API', time: new Date() });
});

app.get('/api/notes', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM notes ORDER BY id DESC');
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/notes', async (req, res) => {
  const { title } = req.body;
  if (!title) return res.status(400).json({ error: 'title es requerido' });
  try {
    const result = await pool.query('INSERT INTO notes (title) VALUES ($1) RETURNING *', [title]);
    res.status(201).json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(port, () => {
  console.log(`Node API escuchando en el puerto ${port}`);
});
