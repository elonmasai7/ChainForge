from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import os

app = FastAPI(title="CreatorChain Auth Service")
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
OAUTH_GOOGLE_CLIENT_ID = os.getenv("OAUTH_GOOGLE_CLIENT_ID", "")
OAUTH_TWITTER_CLIENT_ID = os.getenv("OAUTH_TWITTER_CLIENT_ID", "")

OAUTH_PROVIDERS = {"google", "twitter", "email"}

class LoginRequest(BaseModel):
    provider: str
    email: str | None = None
    oauth_token: str | None = None

class LoginResponse(BaseModel):
    user_id: str
    wallet_address: str
    access_token: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/login", response_model=LoginResponse)
def login(req: LoginRequest):
    if req.provider not in OAUTH_PROVIDERS:
        raise HTTPException(status_code=400, detail="Unsupported provider")
    # Placeholder: integrate Initia social login wallet tooling here
    user_id = str(uuid.uuid4())
    wallet_address = f"initia1{uuid.uuid4().hex[:20]}"
    access_token = f"devtoken-{uuid.uuid4().hex}"
    return LoginResponse(user_id=user_id, wallet_address=wallet_address, access_token=access_token)

@app.get("/oauth/{provider}/start")
def oauth_start(provider: str):
    if provider not in OAUTH_PROVIDERS:
        raise HTTPException(status_code=400, detail="Unsupported provider")
    # Placeholder URL; replace with provider authorization URL
    client_id = OAUTH_GOOGLE_CLIENT_ID if provider == "google" else OAUTH_TWITTER_CLIENT_ID
    return {"auth_url": f"https://oauth.example.com/{provider}?client_id={client_id}&state={uuid.uuid4().hex}"}

@app.get("/oauth/{provider}/callback", response_model=LoginResponse)
def oauth_callback(provider: str, code: str):
    if provider not in OAUTH_PROVIDERS:
        raise HTTPException(status_code=400, detail="Unsupported provider")
    # Placeholder: exchange code for user info and create Initia wallet
    user_id = str(uuid.uuid4())
    wallet_address = f"initia1{uuid.uuid4().hex[:20]}"
    access_token = f"devtoken-{uuid.uuid4().hex}"
    return LoginResponse(user_id=user_id, wallet_address=wallet_address, access_token=access_token)

@app.get("/wallet/{user_id}")
def get_wallet(user_id: str):
    return {"user_id": user_id, "wallet_address": f"initia1{uuid.uuid4().hex[:20]}"}
