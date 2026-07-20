import os
import time

from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)


def get_db_config():
    """Read database configuration from environment variables."""
    return {
        "host": os.environ.get("DB_HOST", "localhost"),
        "port": os.environ.get("DB_PORT", "5432"),
        "dbname": os.environ.get("DB_NAME", "todos"),
        "user": os.environ.get("DB_USER", "postgres"),
        "password": os.environ.get("DB_PASSWORD", "postgres"),
    }


def get_connection():
    return psycopg2.connect(**get_db_config())


def init_db(retries=10, delay=2):
    """Create the todos table if it does not exist, waiting for the DB to be ready."""
    for attempt in range(1, retries + 1):
        try:
            conn = get_connection()
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        CREATE TABLE IF NOT EXISTS todos (
                            id SERIAL PRIMARY KEY,
                            title TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT NOW()
                        )
                        """
                    )
                conn.commit()
            finally:
                conn.close()
            return
        except Exception as exc:
            print(f"init_db attempt {attempt}/{retries} failed: {exc}", flush=True)
            time.sleep(delay)
    raise RuntimeError("Could not initialize database after multiple attempts")


@app.route("/api/health", methods=["GET"])
def health():
    try:
        conn = get_connection()
        conn.close()
        return jsonify({"status": "ok", "database": "connected"}), 200
    except Exception as exc:
        return jsonify({"status": "error", "database": str(exc)}), 500


@app.route("/api/todos", methods=["GET"])
def list_todos():
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id, title, created_at FROM todos ORDER BY id DESC")
            todos = cur.fetchall()
        return jsonify(todos), 200
    finally:
        conn.close()


@app.route("/api/todos", methods=["POST"])
def create_todo():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400

    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO todos (title) VALUES (%s) RETURNING id, title, created_at",
                (title,),
            )
            todo = cur.fetchone()
        conn.commit()
        return jsonify(todo), 201
    finally:
        conn.close()


@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
            deleted = cur.rowcount
        conn.commit()
        if deleted == 0:
            return jsonify({"error": "todo not found"}), 404
        return jsonify({"message": "deleted", "id": todo_id}), 200
    finally:
        conn.close()


# Initialize the database on import so it works under gunicorn too.
init_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
