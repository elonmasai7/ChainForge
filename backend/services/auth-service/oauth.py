import base64
import hashlib
import os
import urllib.parse
import httpx

OAUTH_REDIRECT_BASE = os.getenv("OAUTH_REDIRECT_BASE", "http://localhost:8001")

GOOGLE_CLIENT_ID = os.getenv("OAUTH_GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("OAUTH_GOOGLE_CLIENT_SECRET", "")

X_CLIENT_ID = os.getenv("OAUTH_TWITTER_CLIENT_ID", "")
X_CLIENT_SECRET = os.getenv("OAUTH_TWITTER_CLIENT_SECRET", "")

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

X_AUTH_URL = "https://x.com/i/oauth2/authorize"
X_TOKEN_URL = "https://api.x.com/2/oauth2/token"
X_USERINFO_URL = "https://api.x.com/2/users/me"

GOOGLE_SCOPE = "openid email profile"
X_SCOPE = os.getenv("OAUTH_TWITTER_SCOPE", "tweet.read users.read offline.access")


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def generate_pkce() -> tuple[str, str]:
    code_verifier = _b64url(os.urandom(32))
    code_challenge = _b64url(hashlib.sha256(code_verifier.encode()).digest())
    return code_verifier, code_challenge


def build_auth_url(provider: str, state: str, code_challenge: str | None = None) -> str:
    redirect_uri = f"{OAUTH_REDIRECT_BASE}/oauth/{provider}/callback"
    if provider == "google":
        params = {
            "client_id": GOOGLE_CLIENT_ID,
            "response_type": "code",
            "scope": GOOGLE_SCOPE,
            "redirect_uri": redirect_uri,
            "state": state,
            "access_type": "offline",
            "prompt": "consent",
        }
        return f"{GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}"
    if provider == "x":
        params = {
            "client_id": X_CLIENT_ID,
            "response_type": "code",
            "scope": X_SCOPE,
            "redirect_uri": redirect_uri,
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }
        return f"{X_AUTH_URL}?{urllib.parse.urlencode(params)}"
    raise ValueError("Unsupported provider")


def exchange_code(provider: str, code: str, code_verifier: str | None = None) -> dict:
    redirect_uri = f"{OAUTH_REDIRECT_BASE}/oauth/{provider}/callback"
    if provider == "google":
        data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }
        resp = httpx.post(GOOGLE_TOKEN_URL, data=data, timeout=10)
        resp.raise_for_status()
        return resp.json()
    if provider == "x":
        data = {
            "code": code,
            "client_id": X_CLIENT_ID,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
            "code_verifier": code_verifier or "",
        }
        headers = {}
        if X_CLIENT_SECRET:
            basic = base64.b64encode(f"{X_CLIENT_ID}:{X_CLIENT_SECRET}".encode()).decode()
            headers["Authorization"] = f"Basic {basic}"
        resp = httpx.post(X_TOKEN_URL, data=data, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    raise ValueError("Unsupported provider")


def fetch_userinfo(provider: str, access_token: str) -> dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    if provider == "google":
        resp = httpx.get(GOOGLE_USERINFO_URL, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    if provider == "x":
        resp = httpx.get(
            X_USERINFO_URL,
            headers=headers,
            params={"user.fields": "profile_image_url,username"},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
    raise ValueError("Unsupported provider")
