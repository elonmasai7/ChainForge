from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
import uuid
import os
import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from shared.db import Base, engine, get_db
from .models import User, OAuthAccount
from .state_store import StateStore
from .oauth import build_auth_url, exchange_code, fetch_userinfo, generate_pkce

app = FastAPI(title="ChainForge Auth Service")
Base.metadata.create_all(bind=engine)

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
OAUTH_GOOGLE_CLIENT_ID = os.getenv("OAUTH_GOOGLE_CLIENT_ID", "")
OAUTH_TWITTER_CLIENT_ID = os.getenv("OAUTH_TWITTER_CLIENT_ID", "")
PRIVY_APP_ID = os.getenv("PRIVY_APP_ID", "")
PRIVY_VERIFICATION_KEY = os.getenv("PRIVY_VERIFICATION_KEY", "")

OAUTH_PROVIDERS = {"google", "x"}
state_store = StateStore()

class LoginRequest(BaseModel):
    provider: str
    email: str | None = None
    oauth_token: str | None = None

class LoginResponse(BaseModel):
    user_id: str
    wallet_address: str
    access_token: str
    provider: str | None = None

class WalletLinkRequest(BaseModel):
    user_id: str
    wallet_address: str

class SessionExchangeRequest(BaseModel):
    privy_access_token: str | None = None
    wallet_address: str | None = None
    email: str | None = None
    name: str | None = None
    avatar_url: str | None = None

class SessionUserResponse(BaseModel):
    user_id: str
    email: str | None = None
    name: str | None = None
    avatar_url: str | None = None
    wallet_address: str | None = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/login", response_model=LoginResponse)
def login(req: LoginRequest):
    if req.provider not in OAUTH_PROVIDERS:
        raise HTTPException(status_code=400, detail="Unsupported provider")
    # Legacy fallback login, not used for OAuth callbacks
    user_id = str(uuid.uuid4())
    wallet_address = f"initia1{uuid.uuid4().hex[:20]}"
    access_token = f"devtoken-{uuid.uuid4().hex}"
    return LoginResponse(user_id=user_id, wallet_address=wallet_address, access_token=access_token, provider=req.provider)

@app.get("/oauth/{provider}/start")
def oauth_start(provider: str):
    if provider not in OAUTH_PROVIDERS:
        raise HTTPException(status_code=400, detail="Unsupported provider")
    code_verifier, code_challenge = generate_pkce()
    state = state_store.put({"provider": provider, "code_verifier": code_verifier})
    auth_url = build_auth_url(provider, state=state, code_challenge=code_challenge)
    return {"auth_url": auth_url}

@app.get("/oauth/{provider}/callback", response_model=LoginResponse)
def oauth_callback(provider: str, code: str, state: str, db: Session = Depends(get_db)):
    if provider not in OAUTH_PROVIDERS:
        raise HTTPException(status_code=400, detail="Unsupported provider")
    state_payload = state_store.get(state)
    if not state_payload or state_payload.get("provider") != provider:
        raise HTTPException(status_code=400, detail="Invalid state")
    state_store.delete(state)

    token_data = exchange_code(provider, code, state_payload.get("code_verifier"))
    access_token = token_data.get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="Missing access token")
    profile = fetch_userinfo(provider, access_token)

    if provider == "google":
        provider_user_id = profile.get("sub")
        email = profile.get("email")
        name = profile.get("name")
        avatar_url = profile.get("picture")
    else:
        provider_user_id = profile.get("data", {}).get("id")
        email = None
        name = profile.get("data", {}).get("name")
        avatar_url = profile.get("data", {}).get("profile_image_url")

    user = db.query(User).filter(User.email == email).first() if email else None
    if not user:
        user = User(email=email, name=name, avatar_url=avatar_url)
        db.add(user)
        db.commit()
        db.refresh(user)

    oauth_account = (
        db.query(OAuthAccount)
        .filter(OAuthAccount.provider == provider, OAuthAccount.provider_user_id == provider_user_id)
        .first()
    )
    if not oauth_account:
        oauth_account = OAuthAccount(
            user_id=user.id,
            provider=provider,
            provider_user_id=provider_user_id,
            access_token=access_token,
            refresh_token=token_data.get("refresh_token"),
            expires_at=str(token_data.get("expires_in")),
        )
        db.add(oauth_account)
        db.commit()

    jwt_token = _create_jwt(user.id)
    return LoginResponse(
        user_id=user.id,
        wallet_address=user.wallet_address or "",
        access_token=jwt_token,
        provider=provider,
    )

@app.post("/wallet/link")
def link_wallet(body: WalletLinkRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == body.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.wallet_address = body.wallet_address
    db.commit()
    return {"status": "linked"}

@app.get("/wallet/{user_id}")
def get_wallet(user_id: str):
    return {"user_id": user_id, "wallet_address": f"initia1{uuid.uuid4().hex[:20]}"}

@app.post("/session/exchange", response_model=LoginResponse)
def session_exchange(
    body: SessionExchangeRequest,
    db: Session = Depends(get_db),
    authorization: str | None = Header(default=None),
):
    if not PRIVY_VERIFICATION_KEY or not PRIVY_APP_ID:
        raise HTTPException(status_code=500, detail="Privy verification not configured")
    token = body.privy_access_token
    if not token and authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
    if not token:
        raise HTTPException(status_code=400, detail="Missing Privy access token")
    try:
        claims = jwt.decode(
            token,
            PRIVY_VERIFICATION_KEY,
            algorithms=["ES256"],
            audience=PRIVY_APP_ID,
            issuer="privy.io",
        )
    except Exception as exc:
        raise HTTPException(status_code=401, detail=f"Invalid Privy token: {exc}") from exc

    privy_did = claims.get("sub")
    if not privy_did:
        raise HTTPException(status_code=400, detail="Privy token missing subject")

    user = db.query(User).filter(User.privy_did == privy_did).first()
    if not user:
        user = User(
            privy_did=privy_did,
            email=body.email,
            name=body.name,
            avatar_url=body.avatar_url,
            wallet_address=body.wallet_address,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        if body.wallet_address:
            user.wallet_address = body.wallet_address
        if body.email and not user.email:
            user.email = body.email
        if body.name and not user.name:
            user.name = body.name
        if body.avatar_url and not user.avatar_url:
            user.avatar_url = body.avatar_url
        db.commit()

    jwt_token = _create_jwt(user.id)
    return LoginResponse(
        user_id=user.id,
        wallet_address=user.wallet_address or "",
        access_token=jwt_token,
        provider="privy",
    )

@app.get("/session/me", response_model=SessionUserResponse)
def session_me(authorization: str | None = Header(default=None), db: Session = Depends(get_db)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1].strip()
    try:
        claims = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except Exception as exc:
        raise HTTPException(status_code=401, detail=f"Invalid token: {exc}") from exc
    user_id = claims.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="Token missing subject")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return SessionUserResponse(
        user_id=user.id,
        email=user.email,
        name=user.name,
        avatar_url=user.avatar_url,
        wallet_address=user.wallet_address,
    )


def _create_jwt(user_id: str) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": user_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=24)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")
