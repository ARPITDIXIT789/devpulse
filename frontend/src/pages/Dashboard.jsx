import { useEffect, useState } from "react";
import ProgressChart from "../components/ProgressChart";
import StatCard from "../components/StatCard";
import StreakBadge from "../components/StreakBadge";
import api from "../api/axios";

function Dashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      const { data } = await api.get("/dashboard/stats");
      setStats(data);
    };
    fetchStats();
  }, []);

  const user = JSON.parse(localStorage.getItem("user") || "{}");

  if (!stats) return <p>Loading dashboard...</p>;

  return (
    <section>
      <h2>Welcome, {user.name || "Developer"}!</h2>
      <div className="grid-4">
        <StatCard value={stats.today_stats.tasks} label="Tasks" />
        <StatCard value={stats.today_stats.commits} label="Commits" />
        <StatCard value={`${stats.today_stats.coding_hours} hr`} label="Coding" />
        <StatCard value={`${stats.today_stats.score}%`} label="Score" />
      </div>
      <ProgressChart data={stats.weekly_progress} />
      <StreakBadge streak={stats.streak} />
    </section>
  );
}

export default Dashboard;
