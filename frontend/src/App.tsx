import { Routes, Route, Link, NavLink, useNavigate } from "react-router-dom";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import StorageDashboard from "./pages/StorageDashboard";
import AdminTasks from "./pages/AdminTasks";
import RequireAuth from "./components/RequireAuth";
import { getCurrentUser, logout, refreshToken } from "./api/client";
import { useState } from "react";

export default function App() {
  const navigate = useNavigate();
  const [_, forceRender] = useState(0);
  const user = getCurrentUser();

  const onLogout = () => {
    logout();
    forceRender((n) => n + 1);
    navigate("/login");
  };

  const onRefresh = async () => {
    try {
      await refreshToken();
      forceRender((n) => n + 1);
    } catch {
      onLogout();
    }
  };

  return (
    <div className="app-root">
      <header className="app-header">
        <Link to="/" className="logo">
          ⚡ Energy Platform
        </Link>

        <nav className="nav">
          <NavLink to="/" className="nav-link">
            Home
          </NavLink>
          <NavLink to="/storage" className="nav-link">
            Storage
          </NavLink>
          <NavLink to="/admin/tasks" className="nav-link">
            Admin
          </NavLink>
        </nav>

        <div className="user-badge">
          {user ? (
            <>
              <span className="user-email">Logged in as {user.sub}</span>
              <button className="btn small" onClick={onRefresh}>
                Refresh token
              </button>
              <button className="btn small" onClick={onLogout}>
                Logout
              </button>
            </>
          ) : (
            <>
              <span className="user-email">Not logged in</span>
              <button className="btn small" onClick={() => navigate("/login")}>
                Login
              </button>
              <button className="btn small" onClick={() => navigate("/register")}>
                Register
              </button>
            </>
          )}
        </div>
      </header>

      <main className="app-main">
        <Routes>
          <Route path="/" element={<HomePage />} />

          <Route
            path="/login"
            element={<LoginPage onLoggedIn={() => forceRender((n) => n + 1)} />}
          />

          <Route path="/register" element={<RegisterPage />} />

          <Route
            path="/storage"
            element={
              <RequireAuth>
                <StorageDashboard />
              </RequireAuth>
            }
          />

          <Route
            path="/admin/tasks"
            element={
              <RequireAuth>
                <AdminTasks />
              </RequireAuth>
            }
          />
        </Routes>
      </main>
    </div>
  );
}
