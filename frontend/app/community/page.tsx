export default function CommunityPage() {
  return (
    <main className="min-h-screen px-8 py-12">
      <div className="badge">AI Coding Guild</div>
      <h1 className="mt-6 text-4xl font-semibold">Build shipping-grade AI tools.</h1>
      <p className="mt-4 text-black/60">
        Join weekly build sessions, private code reviews, and exclusive prompt libraries.
      </p>
      <div className="mt-8 grid gap-6 lg:grid-cols-3">
        <div className="card p-6">
          <h3 className="text-lg font-semibold">Starter</h3>
          <p className="mt-2 text-black/60">$12 / month</p>
          <button className="card mt-4 px-4 py-2">Join</button>
        </div>
        <div className="card p-6">
          <h3 className="text-lg font-semibold">Pro</h3>
          <p className="mt-2 text-black/60">$29 / month</p>
          <button className="card mt-4 px-4 py-2">Join</button>
        </div>
        <div className="card p-6">
          <h3 className="text-lg font-semibold">Studio</h3>
          <p className="mt-2 text-black/60">$79 / month</p>
          <button className="card mt-4 px-4 py-2">Join</button>
        </div>
      </div>
    </main>
  );
}
