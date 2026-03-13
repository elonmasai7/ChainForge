import Link from "next/link";

export default function HomePage() {
  return (
    <main className="min-h-screen px-8 py-12">
      <header className="flex items-center justify-between">
        <div className="text-2xl font-semibold">CreatorChain</div>
        <nav className="flex gap-6 text-sm">
          <Link href="/dashboard">Creator Dashboard</Link>
          <Link href="/community">Community Page</Link>
          <Link href="/analytics">Analytics</Link>
          <Link href="/login">Login</Link>
        </nav>
      </header>

      <section className="mt-16 grid gap-8 lg:grid-cols-2">
        <div>
          <div className="badge">Initia Appchain</div>
          <h1 className="mt-6 text-5xl font-semibold leading-tight">
            Launch a revenue engine for your community in minutes.
          </h1>
          <p className="mt-6 text-lg text-black/70">
            CreatorChain spins up mini-platforms with subscriptions, micropayments,
            paid AI tools, and cross-ecosystem onboarding powered by Initia.
          </p>
          <div className="mt-8 flex gap-4">
            <Link className="card px-6 py-3" href="/dashboard">Start a Platform</Link>
            <Link className="card px-6 py-3" href="/community">View Demo Community</Link>
          </div>
        </div>
        <div className="card p-8">
          <div className="text-sm uppercase tracking-[0.3em] text-black/50">Live Pulse</div>
          <div className="mt-6 grid gap-4">
            <div className="card p-4">
              <div className="text-sm text-black/50">Today’s Revenue</div>
              <div className="text-3xl font-semibold">$4,392</div>
            </div>
            <div className="card p-4">
              <div className="text-sm text-black/50">Active Subscribers</div>
              <div className="text-3xl font-semibold">1,284</div>
            </div>
            <div className="card p-4">
              <div className="text-sm text-black/50">Top Product</div>
              <div className="text-xl font-semibold">AI Code Review Lab</div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
