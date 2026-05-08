import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

function ProgressChart({ data }) {
  return (
    <div className="card chart-box">
      <h3>Weekly Progress</h3>
      <ResponsiveContainer width="100%" height={260}>
        <LineChart data={data}>
          <XAxis dataKey="date" hide={false} />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Line type="monotone" dataKey="tasks" stroke="#3fb950" strokeWidth={3} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ProgressChart;
