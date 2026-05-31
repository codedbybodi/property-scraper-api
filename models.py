from sqlalchemy  import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from db import Base


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=True)
    area_m2 = Column(Float, nullable=True)
    location = Column(String, nullable=True)
    bedrooms = Column(Integer, nullable=True)
    property_type = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    scraped_at = Column(DateTime, default=func.now())

class MarketInsight(Base):
    __tablename__ = "market_insights"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=False)
    avg_price = Column(Float, nullable=True)
    avg_price_per_m2 = Column(Float, nullable=False)
    total_listings = Column(Integer, nullable=True)
    ai_analysis = Column(Text, nullable=True)
    generated_at = Column(DateTime, default=func.now())
