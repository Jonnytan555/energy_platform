export default function AdminTasks() {
  return (
    <div>
      <h2>🛠️ Admin</h2>

      <p style={{ color: "#666", marginTop: 10 }}>
        Admin task monitoring is not enabled yet.
      </p>

      <p style={{ color: "#666" }}>
        When Celery is added, this page will show:
      </p>

      <ul>
        <li>Active background tasks</li>
        <li>Worker health</li>
        <li>Scrape job status</li>
      </ul>
    </div>
  );
}
