from fastapi import FastAPI, HTTPException, Depends
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

app = FastAPI(title="CreatorChain Auth Service")
Base.metadata.create_all(bind=engine)

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
OAUTH_GOOGLE_CLIENT_ID = os.getenv("OAUTH_GOOGLE_CLIENT_ID", "")
OAUTH_TWITTER_CLIENT_ID = os.getenv("OAUTH_TWITTER_CLIENT_ID", "")

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


def _create_jwt(user_id: str) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": user_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=24)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")
