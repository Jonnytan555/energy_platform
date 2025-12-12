import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { register, login } from "../api/client";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    setLoading(true);

    try {
      await register(email, password);
      // Auto-login after register (nice UX)
      await login(email, password);
      navigate("/storage");
    } catch (e: any) {
      const msg = e?.response?.data?.detail || "Registration failed.";
      setErr(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Register</h2>

      <form onSubmit={onSubmit} className="form">
        <label>Email</label>
        <input value={email} onChange={(e) => setEmail(e.target.value)} />

        <label>Password</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />

        {err && <div className="error">{err}</div>}

        <button className="btn" disabled={loading}>
          {loading ? "Creating..." : "Create account"}
        </button>

        <div style={{ marginTop: 10, fontSize: 14 }}>
          Already have an account? <Link to="/login">Login</Link>
        </div>
      </form>
    </div>
  );
}
