function TaskCard({ task, onDelete, onStatus }) {
  return (
    <div className="card task-card">
      <div>
        <h3>{task.title}</h3>
        <p>{task.description || "No description"}</p>
      </div>
      <div className="task-actions">
        <span className={`badge ${task.status}`}>{task.status}</span>
        <button onClick={() => onStatus(task)} className="ghost">Toggle</button>
        <button onClick={() => onDelete(task.id)} className="danger">Delete</button>
      </div>
    </div>
  );
}

export default TaskCard;
