import { useEffect, useState } from "react";

// API base URL comes from an environment variable at build time.
// Falls back to "/api" which works with the Vite dev proxy and Nginx.
const API_URL = import.meta.env.VITE_API_URL || "/api";

export default function App() {
  const [todos, setTodos] = useState([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState("");

  async function loadTodos() {
    try {
      const res = await fetch(`${API_URL}/todos`);
      if (!res.ok) throw new Error("Failed to load todos");
      setTodos(await res.json());
      setError("");
    } catch (err) {
      setError(err.message);
    }
  }

  async function addTodo(e) {
    e.preventDefault();
    const value = title.trim();
    if (!value) return;
    try {
      const res = await fetch(`${API_URL}/todos`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: value }),
      });
      if (!res.ok) throw new Error("Failed to add todo");
      setTitle("");
      loadTodos();
    } catch (err) {
      setError(err.message);
    }
  }

  async function deleteTodo(id) {
    try {
      const res = await fetch(`${API_URL}/todos/${id}`, { method: "DELETE" });
      if (!res.ok) throw new Error("Failed to delete todo");
      loadTodos();
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadTodos();
  }, []);

  return (
    <div className="container">
      <h1>Todo App</h1>

      <form onSubmit={addTodo} className="add-form">
        <input
          type="text"
          value={title}
          placeholder="What needs to be done?"
          onChange={(e) => setTitle(e.target.value)}
        />
        <button type="submit">Add</button>
      </form>

      {error && <p className="error">{error}</p>}

      <ul className="todo-list">
        {todos.length === 0 && <li className="empty">No todos yet.</li>}
        {todos.map((todo) => (
          <li key={todo.id} className="todo-item">
            <span>{todo.title}</span>
            <button onClick={() => deleteTodo(todo.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
