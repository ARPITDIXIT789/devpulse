import { useEffect, useState } from "react";
import api from "../api/axios";
import TaskCard from "../components/TaskCard";

function Tasks() {
  const [tasks, setTasks] = useState([]);
  const [form, setForm] = useState({ title: "", description: "", status: "pending" });

  const loadTasks = async () => {
    const { data } = await api.get("/tasks");
    setTasks(data);
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const addTask = async (e) => {
    e.preventDefault();
    await api.post("/tasks", form);
    setForm({ title: "", description: "", status: "pending" });
    loadTasks();
  };

  const deleteTask = async (id) => {
    await api.delete(`/tasks/${id}`);
    loadTasks();
  };

  const toggleStatus = async (task) => {
    const next = task.status === "done" ? "pending" : "done";
    await api.put(`/tasks/${task.id}`, { ...task, status: next });
    loadTasks();
  };

  return (
    <section>
      <h2>My Tasks</h2>
      <form className="task-form" onSubmit={addTask}>
        <input value={form.title} placeholder="Task title" onChange={(e) => setForm({ ...form, title: e.target.value })} required />
        <input value={form.description} placeholder="Description" onChange={(e) => setForm({ ...form, description: e.target.value })} />
        <select value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
        </select>
        <button type="submit">Add Task</button>
      </form>
      <div className="stack">
        {tasks.map((task) => (
          <TaskCard key={task.id} task={task} onDelete={deleteTask} onStatus={toggleStatus} />
        ))}
      </div>
    </section>
  );
}

export default Tasks;
