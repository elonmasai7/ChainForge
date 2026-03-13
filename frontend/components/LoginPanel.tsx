"use client";

import { useEffect } from "react";
import { useCreateWallet, usePrivy, useWallets, useLoginWithOAuth } from "@privy-io/react-auth";

export function LoginPanel() {
  const { ready, authenticated, user, logout } = usePrivy();
  const { wallets } = useWallets();
  const { createWallet } = useCreateWallet();
  const { initOAuth } = useLoginWithOAuth();

  useEffect(() => {
    if (ready && authenticated && wallets.length === 0) {
      createWallet();
    }
  }, [ready, authenticated, wallets.length, createWallet]);

  if (!ready) return <div className="card p-6">Loading...</div>;

  return (
    <div className="card p-6">
      <h2 className="text-xl font-semibold">Sign in</h2>
      {!authenticated ? (
        <div className="mt-4 grid gap-3">
          <button className="card px-4 py-2" onClick={() => initOAuth({ provider: "google" })}>
            Continue with Google
          </button>
          <button className="card px-4 py-2" onClick={() => initOAuth({ provider: "twitter" })}>
            Continue with X
          </button>
        </div>
      ) : (
        <div className="mt-4 space-y-3 text-sm">
          <div>Logged in as: {user?.email || user?.id}</div>
          <div>Wallet: {wallets[0]?.address || "creating..."}</div>
          <button className="card px-4 py-2" onClick={logout}>Sign out</button>
        </div>
      )}
    </div>
  );
}
