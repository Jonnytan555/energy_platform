export default function HomePage() {
  return (
    <section className="card">
      <h1>⚡ Energy Analytics Platform</h1>
      <p>
        This is your full-stack platform: FastAPI backend (scrapers, storage, curves), Celery workers for background jobs,
        and React UI for dashboards.
      </p>

      <ul>
        <li>📦 Storage (AGSI / ALSI / EIA)</li>
        <li>🧵 Background scrapes via Celery</li>
        <li>🔐 JWT bearer auth on all endpoints</li>
      </ul>
    </section>
  );
}
