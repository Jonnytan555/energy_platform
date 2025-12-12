import { useState } from "react";
import AgsiTab from "./AgsiTab";
import AlsiTab from "./AlsiTab";

export default function StorageDashboard() {
  const [tab, setTab] = useState<"agsi" | "alsi">("agsi");

  return (
    <div>
      <h1>📦 Storage</h1>

      <div style={{ display: "flex", gap: 10, marginBottom: 16 }}>
        <button onClick={() => setTab("agsi")} style={{ fontWeight: tab === "agsi" ? 700 : 400 }}>
          AGSI (Gas)
        </button>

        <button onClick={() => setTab("alsi")} style={{ fontWeight: tab === "alsi" ? 700 : 400 }}>
          ALSI (LNG)
        </button>
      </div>

      {tab === "agsi" ? <AgsiTab /> : <AlsiTab />}
    </div>
  );
}
