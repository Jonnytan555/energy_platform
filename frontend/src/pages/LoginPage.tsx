import { useState } from "react";
import { useLocation, useNavigate, Link } from "react-router-dom";
import { login } from "../api/client";

export default function LoginPage({ onLoggedIn }: { onLoggedIn?: () => void }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();
  const location = useLocation() as any;
  const from = location?.state?.from || "/storage";

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    setLoading(true);
    try {
      await login(email, password);
      onLoggedIn?.();
      navigate(from);
    } catch (e: any) {
      const msg = e?.response?.data?.detail || "Login failed. Check email/password.";
      setErr(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Login</h2>

      <form onSubmit={onSubmit} className="form">
        <label>Email</label>
        <input value={email} onChange={(e) => setEmail(e.target.value)} />

        <label>Password</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />

        {err && <div className="error">{err}</div>}

        <button className="btn" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>

        <div style={{ marginTop: 10, fontSize: 14 }}>
          No account? <Link to="/register">Register</Link>
        </div>
      </form>
    </div>
  );
}
