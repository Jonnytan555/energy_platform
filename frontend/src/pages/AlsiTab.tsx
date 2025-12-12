import { useEffect, useMemo, useState } from "react";
import { fetchAlsiLatest, scrapeAlsi, type AlsiLatestRow } from "../api/client";

export default function AlsiTab() {
  const [country, setCountry] = useState("EU");
  const [limit, setLimit] = useState<number>(365);
  const [rows, setRows] = useState<AlsiLatestRow[]>([]);
  const [status, setStatus] = useState<string>("");

  const loadLatestFromDb = async () => {
    setStatus("Loading latest ALSI from DB...");
    try {
      const data = await fetchAlsiLatest(limit);
      setRows(data);
      setStatus(`Loaded ${data.length} latest rows (is_latest=true)`);
    } catch (e: any) {
      setStatus(e?.response?.data?.detail ?? "Failed to load ALSI latest");
    }
  };

  const scrapeAndRefresh = async () => {
    setStatus("Scraping ALSI + persisting...");
    try {
      // backend scrape returns { rows_persisted, data } but we want DB latest after persist
      await scrapeAlsi(country);
      await loadLatestFromDb();
      setStatus("Scraped + refreshed latest ALSI rows");
    } catch (e: any) {
      setStatus(e?.response?.data?.detail ?? "ALSI scrape failed");
    }
  };

  useEffect(() => {
    loadLatestFromDb();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const sorted = useMemo(() => {
    return [...rows].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
  }, [rows]);

  // handle either inventory_gwh or lng_storage_gwh depending on your response handler/model
  const storageVal = (r: AlsiLatestRow) => r.inventory_gwh ?? r.lng_storage_gwh ?? "";

  return (
    <div>
      <h2>🧊 ALSI LNG Storage (DB Latest Only)</h2>

      <div style={{ display: "flex", gap: 12, alignItems: "end", marginBottom: 12 }}>
        <div>
          <div>Country (for scrape)</div>
          <select value={country} onChange={(e) => setCountry(e.target.value)}>
            <option value="EU">EU</option>
            <option value="GB">GB</option>
            <option value="FR">FR</option>
            <option value="ES">ES</option>
            <option value="NL">NL</option>
          </select>
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
            <th>Inventory / Storage (GWh)</th>
            <th>SendOut</th>
            <th>DTMI (GWh)</th>
            <th>DTRS</th>
            <th>Created Date (DB)</th>
          </tr>
        </thead>
        <tbody>
          {sorted.slice(0, 200).map((r, i) => (
            <tr key={i} style={i === 0 ? { fontWeight: "bold" } : {}}>
              <td>{r.date}</td>
              <td>{storageVal(r)}</td>
              <td>{r.sendOut ?? ""}</td>
              <td>{r.dtmi_gwh ?? ""}</td>
              <td>{r.dtrs ?? ""}</td>
              <td>{r.created_date ?? ""}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
