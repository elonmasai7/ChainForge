import { NextRequest, NextResponse } from "next/server";

const AUTH_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8001";
const COOKIE_NAME = "creatorchain_jwt";

export async function POST(req: NextRequest) {
  const body = await req.json();
  const response = await fetch(`${AUTH_BASE}/session/exchange`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const errorText = await response.text();
    return NextResponse.json({ error: errorText }, { status: response.status });
  }

  const data = await response.json();
  const res = NextResponse.json({ ok: true, user: data.user_id });
  res.cookies.set({
    name: COOKIE_NAME,
    value: data.access_token,
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    path: "/",
    maxAge: 60 * 60 * 24,
  });
  return res;
}
