from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from shared.db import get_db
import asyncio
from fastapi.responses import StreamingResponse
import json

app = FastAPI(title="ChainForge Analytics Service")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/revenue/summary")
def revenue_summary(platform_id: str, db: Session = Depends(get_db)):
    query = text(
        "SELECT COALESCE(SUM(amount), 0) AS total, COUNT(*) AS txs "
        "FROM payments WHERE platform_id = :platform_id"
    )
    result = db.execute(query, {"platform_id": platform_id}).fetchone()
    return {"platform_id": platform_id, "total": float(result.total), "transactions": result.txs}

@app.get("/subscriptions/active")
def active_subscriptions(platform_id: str, db: Session = Depends(get_db)):
    query = text(
        "SELECT COUNT(*) AS active_count FROM subscriptions "
        "WHERE platform_id = :platform_id AND status = 'active'"
    )
    result = db.execute(query, {"platform_id": platform_id}).fetchone()
    return {"platform_id": platform_id, "active": result.active_count}

@app.get("/revenue/stream")
def revenue_stream(platform_id: str, db: Session = Depends(get_db)):
    async def event_generator():
        while True:
            query = text(
                "SELECT COALESCE(SUM(amount), 0) AS total, COUNT(*) AS txs "
                "FROM payments WHERE platform_id = :platform_id"
            )
            result = db.execute(query, {"platform_id": platform_id}).fetchone()
            payload = {"platform_id": platform_id, "total": float(result.total), "transactions": result.txs}
            yield f"data: {json.dumps(payload)}\\n\\n"
            await asyncio.sleep(2)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
