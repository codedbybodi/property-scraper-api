import os
import pandas as pd
from google import genai
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import models

load_dotenv()
Client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def analyze_market(db: Session, location: str = None) -> dict:
    query = db.query(models.Property)
    if location:
        query = query.filter(models.Property.location.ilike(f"%{location}"))

    properties = query.all()
    if not properties:
        return {"error": "No properties found"}
    
    data = [{
        "title": p.title,
        "price": p.price,
        "area_m2": p.area_m2,
        "location": p.location,
        "bedrooms": p.bedrooms,
        "property_type": p.property_type
    } for p in properties if p.price]

    if not data:
        return {"error": "No Properties with prices found. Re-run scraper after fixing price extraction."}


    df = pd.DataFrame(data)

    avg_price = round(df["price"].mean(), 2)
    max_price = df["price"].max()
    min_price = df["price"].min()
    avg_area = round(df["area_m2"].mean(), 2) if df["area_m2"].notna().any() else 0
    avg_price_per_m2 = round(avg_price / avg_area, 2) if avg_area > 0 else 0
    total = len(df)
    by_type = df.groupby("property_type")["price"].mean().round(2).to_dict()

    prompt = f"""
You are a real estate market analyst for Egypt.

Here is REAL mareket data scraped from Egyption property market for {location or 'All Egypt'}:

- Total listings: {total}
- Average price: {avg_price:,.0f} EGP
- Highest price: {max_price:,.0f} EGP
- Lowest price: {min_price:,.0f} EGP
- Averge price per meter: {avg_price_per_m2:,.0f} EGP/m²
- Averge price by property type: {by_type}

Based on THIS specific data, Give a short 3-paragraph market analysis:
1. Current market overview
2. Investment potential
3. Recommendation for buyers and investores
"""
    response = Client.models.generate_content(model="gemini-3-flash-preview", contents=prompt)
    return{"location": location or "Cairo", "total_listings": total, "avg_price": round(avg_price, 2), "max_price": max_price, "min_price": min_price, "avg_area_m2": avg_area, "avg_price_per_m2": avg_price_per_m2, "avg_by_type": by_type, "ai_analysis": response.text}

    