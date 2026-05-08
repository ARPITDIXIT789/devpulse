function StatCard({ value, label }) {
  return (
    <div className="card stat-card">
      <h2>{value}</h2>
      <p>{label}</p>
    </div>
  );
}

export default StatCard;
