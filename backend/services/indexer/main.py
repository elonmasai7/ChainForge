from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from shared.db import get_db
import uuid
import json
import os
import httpx

app = FastAPI(title="ChainForge Indexer")
INITIA_RPC_URL = os.getenv("INITIA_RPC_URL", "http://localhost:26657")
INITIA_TX_SEARCH_QUERY = os.getenv("INITIA_TX_SEARCH_QUERY", "")

class ChainEvent(BaseModel):
    event_type: str
    payload: dict

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/events")
def ingest_event(event: ChainEvent, db: Session = Depends(get_db)):
    query = text(
        "INSERT INTO events (id, event_type, payload) VALUES (:id, :event_type, :payload)"
    )
    db.execute(
        query,
        {
            "id": str(uuid.uuid4()),
            "event_type": event.event_type,
            "payload": json.dumps(event.payload),
        },
    )
    db.commit()
    return {"status": "indexed"}

@app.get("/sync/latest")
def sync_latest(db: Session = Depends(get_db)):
    """
    Minimal RPC sync stub. Replace with Initia event streaming or tx_search.
    """
    base = INITIA_RPC_URL.rstrip("/")
    with httpx.Client(timeout=10) as client:
        if INITIA_TX_SEARCH_QUERY:
            resp = client.get(
                f"{base}/tx_search",
                params={"query": INITIA_TX_SEARCH_QUERY, "prove": "false"},
            )
            resp.raise_for_status()
            payload = resp.json()
            event_type = "initia_tx_search"
        else:
            client.post(f"{base}/health", json={})
            payload = {"status": "ok"}
            event_type = "initia_sync"

    query = text("INSERT INTO events (id, event_type, payload) VALUES (:id, :event_type, :payload)")
    db.execute(
        query,
        {"id": str(uuid.uuid4()), "event_type": event_type, "payload": json.dumps(payload)},
    )
    db.commit()
    return {"status": "synced"}
