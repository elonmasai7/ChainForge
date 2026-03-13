import { LoginPanel } from "@/components/LoginPanel";

export default function LoginPage() {
  return (
    <main className="min-h-screen px-8 py-12">
      <h1 className="text-4xl font-semibold">ChainForge Login</h1>
      <div className="mt-8 max-w-md">
        <LoginPanel />
      </div>
    </main>
  );
}
