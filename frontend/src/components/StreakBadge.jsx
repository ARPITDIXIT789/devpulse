function StreakBadge({ streak }) {
  return (
    <div className="card streak">
      <h3>Streak</h3>
      <p>{streak?.current_streak || 0} Days</p>
      <small>Best: {streak?.best_streak || 0} Days</small>
    </div>
  );
}

export default StreakBadge;
