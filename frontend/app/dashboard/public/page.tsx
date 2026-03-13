export default function PublicDashboardLanding() {
  return (
    <main className="min-h-screen px-8 py-12">
      <div className="badge">Public Preview</div>
      <h1 className="mt-6 text-4xl font-semibold">ChainForge Public Dashboard</h1>
      <p className="mt-4 text-black/60">
        This page bypasses auth middleware. Share it as a teaser for your creator community.
      </p>
    </main>
  );
}
