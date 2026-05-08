import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  const theme = localStorage.getItem("theme") || "dark";

  const toggleTheme = () => {
    const next = document.documentElement.dataset.theme === "light" ? "dark" : "light";
    document.documentElement.dataset.theme = next;
    localStorage.setItem("theme", next);
  };

  if (!document.documentElement.dataset.theme) {
    document.documentElement.dataset.theme = theme;
  }

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/login");
  };

  return (
    <header className="nav">
      <h1>DevPulse</h1>
      <nav>
        {token && <Link to="/">Dashboard</Link>}
        {token && <Link to="/tasks">Tasks</Link>}
        {token && <Link to="/profile">Profile</Link>}
        <button onClick={toggleTheme} className="ghost">Theme</button>
        {token ? (
          <button onClick={logout}>Logout</button>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/signup">Signup</Link>
          </>
        )}
      </nav>
    </header>
  );
}

export default Navbar;
