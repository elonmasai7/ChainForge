import { NextRequest, NextResponse } from "next/server";

const AUTH_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8001";
const COOKIE_NAME = "creatorchain_jwt";

export async function middleware(req: NextRequest) {
  const pathname = req.nextUrl.pathname;
  if (
    pathname.startsWith("/login") ||
    pathname.startsWith("/community") ||
    pathname.startsWith("/payment") ||
    pathname.endsWith("/health") ||
    pathname.startsWith("/dashboard/public") ||
    pathname.startsWith("/analytics/public")
  ) {
    return NextResponse.next();
  }

  const token = req.cookies.get(COOKIE_NAME)?.value;
  if (!token) {
    return NextResponse.redirect(new URL("/login", req.url));
  }

  const res = await fetch(`${AUTH_BASE}/session/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!res.ok) {
    return NextResponse.redirect(new URL("/login", req.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/analytics/:path*"],
};
