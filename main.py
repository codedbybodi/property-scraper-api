from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
from db import get_db, engine
from services.scraper import scrape_aqarmap
from services.ai import analyze_market
from typing import Optional
import models

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Property Screaper & Market Analyzwe", version="1.0.0")

# Scheduler - Runs Scraper every 24 hours
scheduler = BackgroundScheduler()

def scheduled_scrape():
    from db import SessionLocal
    db = SessionLocal()
    try:
        count = scrape_aqarmap(db)
        print(f"Scheduled scrape: {count} new properties added")
    finally:
        db.close()

scheduler.add_job(scheduled_scrape, "interval", hours=24)
scheduler.start()


# Routes 
@app.get("/", tags="Health")
def home():
    return{"status": "running", "message": "Property Scraper API"}

@app.post("/scrape", tags=["Scraper"])
def trigger_scrape(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    count = scrape_aqarmap(db)
    return {"message": f"Scrape Complete", "new_properties": count}

@app.get("/properties", tags=["Properties"])
def get_properties(
    location: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    bedrooms: Optional[int] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    query = db.query(models.Property)
    if location:
        query = query.filter(models.Property.location.ilike(f"%{location}"))
    if min_price:
        query = query.filter(models.Property.price >= min_price)
    if max_price:
        query = query.filter(models.Property.price <= max_price)
    if bedrooms:
        query = query.filter(models.Property.bedrooms == bedrooms)
    return query.offset(skip).limit(limit).all()

@app.get("/properties/count", tags=["Properties"])
def count_properties(db: Session = Depends(get_db)):
    count = db.query(models.Property).count()
    return {"total_properties": count}

@app.get("/analyze", tags=["AI analysis"])
def market_analysis(location: Optional[str] = None, db: Session = Depends(get_db)):
    return analyze_market(db, location)