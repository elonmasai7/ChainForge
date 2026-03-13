"use client";

import { useEffect, useRef, useState } from "react";
import { useCreateWallet, usePrivy, useWallets, useLoginWithOAuth } from "@privy-io/react-auth";

export function LoginPanel() {
  const { ready, authenticated, user, logout } = usePrivy();
  const { wallets } = useWallets();
  const { createWallet } = useCreateWallet();
  const { initOAuth } = useLoginWithOAuth();
  const [exchangeStatus, setExchangeStatus] = useState<string | null>(null);
  const [logoutStatus, setLogoutStatus] = useState<string | null>(null);
  const exchanged = useRef(false);

  useEffect(() => {
    if (ready && authenticated && wallets.length === 0) {
      createWallet();
    }
  }, [ready, authenticated, wallets.length, createWallet]);

  useEffect(() => {
    const runExchange = async () => {
      if (!ready || !authenticated || exchanged.current) return;
      const walletAddress = wallets[0]?.address;
      if (!walletAddress) return;
      try {
        const accessToken = await user?.getAccessToken?.();
        if (!accessToken) return;
        setExchangeStatus("Syncing session...");
        const res = await fetch("/api/session/exchange", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            privy_access_token: accessToken,
            wallet_address: walletAddress,
            email: user?.email,
            name: user?.name,
            avatar_url: user?.avatarUrl,
          }),
        });
        if (!res.ok) {
          setExchangeStatus("Session sync failed");
          return;
        }
        exchanged.current = true;
        setExchangeStatus("Session synced");
      } catch {
        setExchangeStatus("Session sync failed");
      }
    };
    runExchange();
  }, [ready, authenticated, wallets, user]);

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
          {exchangeStatus ? <div>{exchangeStatus}</div> : null}
          {logoutStatus ? <div>{logoutStatus}</div> : null}
          <button
            className="card px-4 py-2"
            onClick={async () => {
              setLogoutStatus(null);
              await fetch("/api/session/logout", { method: "POST" });
              await logout();
              setLogoutStatus("Signed out");
            }}
          >
            Sign out
          </button>
        </div>
      )}
    </div>
  );
}
