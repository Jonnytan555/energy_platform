import { useEffect, useMemo, useState } from "react";
import { fetchAgsiLatest, scrapeAgsiSync, type AgsiLatestRow } from "../api/client";

export default function AgsiTab() {
  const [zone, setZone] = useState("eu"); // API zone for scrape
  const [pages, setPages] = useState<number>(30);
  const [limit, setLimit] = useState<number>(365); // DB rows to show
  const [rows, setRows] = useState<AgsiLatestRow[]>([]);
  const [status, setStatus] = useState<string>("");

  const loadLatestFromDb = async () => {
    setStatus("Loading latest from DB...");
    try {
      // currently DB endpoint uses eu in path; keep it consistent for now
      const data = await fetchAgsiLatest(limit);
      setRows(data);
      setStatus(`Loaded ${data.length} latest rows (is_latest=true)`);
    } catch (e: any) {
      setStatus(e?.response?.data?.detail ?? "Failed to load DB latest");
    }
  };

  const scrapeAndRefresh = async () => {
    setStatus("Scraping (API) + persisting...");
    try {
      await scrapeAgsiSync(zone, pages);
      await loadLatestFromDb();
      setStatus(`Scraped + refreshed latest rows`);
    } catch (e: any) {
      setStatus(e?.response?.data?.detail ?? "Scrape failed");
    }
  };

  useEffect(() => {
    loadLatestFromDb();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const sorted = useMemo(() => {
    // backend already returns desc, but keep safe
    return [...rows].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
  }, [rows]);

  return (
    <div>
      <h2>📦 AGSI Storage (DB Latest Only)</h2>

      <div style={{ display: "flex", gap: 12, alignItems: "end", marginBottom: 12 }}>
        <div>
          <div>Zone (for scrape)</div>
          <select value={zone} onChange={(e) => setZone(e.target.value)}>
            <option value="eu">EU</option>
            <option value="de">DE</option>
            <option value="fr">FR</option>
          </select>
        </div>

        <div>
          <div>Pages (scrape)</div>
          <input
            type="number"
            min={1}
            value={pages}
            onChange={(e) => setPages(Number(e.target.value))}
            style={{ width: 110 }}
          />
        </div>

        <div>
          <div>DB rows (limit)</div>
          <input
            type="number"
            min={1}
            max={5000}
            value={limit}
            onChange={(e) => setLimit(Number(e.target.value))}
            style={{ width: 110 }}
          />
        </div>

        <button onClick={loadLatestFromDb}>Fetch latest</button>
        <button onClick={scrapeAndRefresh}>Scrape + refresh</button>
      </div>

      <div style={{ marginBottom: 12 }}>{status}</div>

      <table width="100%" border={1} cellPadding={8}>
        <thead>
          <tr>
            <th>Date</th>
            <th>% Full</th>
            <th>Gas (GWh)</th>
            <th>Injection</th>
            <th>Withdrawal</th>
            <th>Created Date (DB)</th>
          </tr>
        </thead>
        <tbody>
          {sorted.slice(0, 200).map((r, i) => (
            <tr key={i} style={i === 0 ? { fontWeight: "bold" } : {}}>
              <td>{r.date}</td>
              <td>{r.full_pct ?? ""}</td>
              <td>{r.gas_in_storage_gwh ?? ""}</td>
              <td>{r.injection ?? ""}</td>
              <td>{r.withdrawal ?? ""}</td>
              <td>{r.created_date ?? ""}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
