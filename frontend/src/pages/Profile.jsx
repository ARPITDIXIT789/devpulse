import { useEffect, useState } from "react";
import api from "../api/axios";

function Profile() {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    const load = async () => {
      const { data } = await api.get("/profile");
      setProfile(data);
    };
    load();
  }, []);

  if (!profile) return <p>Loading profile...</p>;

  return (
    <section className="card profile-card">
      <h2>{profile.user.name}</h2>
      <p>{profile.user.email}</p>
      <hr />
      <p>Total Tasks: {profile.stats.total_tasks}</p>
      <p>Completed Tasks: {profile.stats.completed_tasks}</p>
      <p>Completion Rate: {profile.stats.completion_rate}%</p>
      <p>Current Streak: {profile.stats.current_streak} days</p>
      <p>Best Streak: {profile.stats.best_streak} days</p>
    </section>
  );
}

export default Profile;
