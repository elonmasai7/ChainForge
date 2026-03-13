from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from shared.db import Base, engine, get_db
from .models import Subscription, Payment
from .rpc import InitiaRPCClient

app = FastAPI(title="CreatorChain Payment Service")
Base.metadata.create_all(bind=engine)
rpc = InitiaRPCClient()

class SubscriptionIn(BaseModel):
    platform_id: str
    user_id: str
    price_amount: float
    price_denom: str

class PaymentIn(BaseModel):
    platform_id: str
    user_id: str
    amount: float
    denom: str
    tx_hash: str | None = None
    route_to_creator: bool = True

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/subscriptions")
def create_subscription(body: SubscriptionIn, db: Session = Depends(get_db)):
    sub = Subscription(**body.model_dump(), status="active")
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub

@app.post("/payments")
def create_payment(body: PaymentIn, db: Session = Depends(get_db)):
    if body.route_to_creator:
        try:
            tx_hash = rpc.route_revenue(platform_id=body.platform_id, amount=body.amount, denom=body.denom)
        except Exception as exc:
            raise HTTPException(status_code=502, detail=f"Initia RPC error: {exc}") from exc
        payload = body.model_dump()
        payload["tx_hash"] = tx_hash
        payment = Payment(**payload)
    else:
        payment = Payment(**body.model_dump())
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment
