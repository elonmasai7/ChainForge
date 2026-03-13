from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from shared.db import Base, engine, get_db
from .models import Creator, Platform

app = FastAPI(title="ChainForge Creator Service")
Base.metadata.create_all(bind=engine)

class CreatorIn(BaseModel):
    name: str
    handle: str
    wallet_address: str

class PlatformIn(BaseModel):
    creator_id: str
    name: str
    monetization_type: str
    pricing_model: dict

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/creators")
def create_creator(body: CreatorIn, db: Session = Depends(get_db)):
    creator = Creator(**body.model_dump())
    db.add(creator)
    db.commit()
    db.refresh(creator)
    return creator

@app.post("/platforms")
def create_platform(body: PlatformIn, db: Session = Depends(get_db)):
    platform = Platform(**body.model_dump())
    db.add(platform)
    db.commit()
    db.refresh(platform)
    return platform

@app.get("/creators/{creator_id}")
def get_creator(creator_id: str, db: Session = Depends(get_db)):
    return db.query(Creator).filter(Creator.id == creator_id).first()

@app.get("/platforms/{platform_id}")
def get_platform(platform_id: str, db: Session = Depends(get_db)):
    return db.query(Platform).filter(Platform.id == platform_id).first()
