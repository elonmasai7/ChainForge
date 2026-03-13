export default function DashboardPage() {
  return (
    <main className="min-h-screen px-8 py-12">
      <div className="flex items-center justify-between">
        <h1 className="text-4xl font-semibold">Creator Dashboard</h1>
        <a className="badge" href="/dashboard/public">Public Preview</a>
      </div>
      <section className="mt-8 grid gap-6 lg:grid-cols-3">
        <div className="card p-6">
          <div className="text-sm text-black/50">Revenue Today</div>
          <div className="text-3xl font-semibold">$1,240</div>
        </div>
        <div className="card p-6">
          <div className="text-sm text-black/50">Active Plans</div>
          <div className="text-3xl font-semibold">3</div>
        </div>
        <div className="card p-6">
          <div className="text-sm text-black/50">Churn Risk</div>
          <div className="text-3xl font-semibold">Low</div>
        </div>
      </section>

      <section className="mt-10 grid gap-8 lg:grid-cols-2">
        <div className="card p-6">
          <h2 className="text-xl font-semibold">Platform Generator</h2>
          <p className="mt-2 text-black/60">
            Create a new revenue stream with prebuilt templates.
          </p>
          <div className="mt-6 grid gap-4">
            <input className="card p-3" placeholder="Project name" />
            <select className="card p-3">
              <option>Paid Community</option>
              <option>Paid AI Tool</option>
              <option>Exclusive Content Hub</option>
              <option>Developer Marketplace</option>
            </select>
            <select className="card p-3">
              <option>Subscription</option>
              <option>Pay-per-content</option>
              <option>Micropayments</option>
              <option>Marketplace Fee</option>
            </select>
            <button className="card px-4 py-3">Generate Platform</button>
          </div>
        </div>
        <div className="card p-6">
          <h2 className="text-xl font-semibold">Recent Transactions</h2>
          <ul className="mt-4 space-y-3 text-sm">
            <li className="card p-3">User initia1c... paid 20 INIT</li>
            <li className="card p-3">User initia1f... subscribed to Pro</li>
            <li className="card p-3">User initia1a... tipped 3 INIT</li>
          </ul>
        </div>
      </section>
    </main>
  );
}
