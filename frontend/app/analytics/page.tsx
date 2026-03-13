\"use client\";

import { useEffect, useState } from \"react\";

type RevenuePayload = { platform_id: string; total: number; transactions: number };

export default function AnalyticsPage() {
  const [data, setData] = useState<RevenuePayload | null>(null);

  useEffect(() => {
    const platformId = \"demo-platform\";
    const base = process.env.NEXT_PUBLIC_ANALYTICS_BASE || process.env.NEXT_PUBLIC_API_BASE || "";
    const source = new EventSource(`${base}/revenue/stream?platform_id=${platformId}`);
    source.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        setData(payload);
      } catch {
        // Ignore malformed payloads
      }
    };
    return () => source.close();
  }, []);

  return (
    <main className=\"min-h-screen px-8 py-12\">
      <h1 className=\"text-4xl font-semibold\">Analytics Dashboard</h1>
      <section className=\"mt-8 grid gap-6 lg:grid-cols-2\">
        <div className=\"card p-6\">
          <h2 className=\"text-lg font-semibold\">Revenue Trend</h2>
          <div className=\"mt-4 text-3xl font-semibold\">
            {data ? `$${data.total}` : \"--\"}
          </div>
          <div className=\"mt-4 h-40 rounded-xl bg-gradient-to-r from-ember/30 to-tide/30\" />
        </div>
        <div className=\"card p-6\">
          <h2 className=\"text-lg font-semibold\">Transactions</h2>
          <div className=\"mt-4 text-3xl font-semibold\">
            {data ? data.transactions : \"--\"}
          </div>
          <div className=\"mt-4 h-40 rounded-xl bg-gradient-to-r from-tide/30 to-ember/30\" />
        </div>
      </section>
    </main>
  );
}
