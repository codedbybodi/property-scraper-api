import requests
import re
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
import models

def extract_price(text: str) -> float:
    if not text:
        return None
    numbers = re.findall(r"\d+", text.replace(",", ""))
    return float(numbers[0]) if numbers else None

def extract_area(text: str) -> float:
    if not text:
        return None
    match = re.search(r"(\d+(?:\.\d+)?)\s*m²?", text, re.IGNORECASE)
    if match:
        return float(match.group(1))
    numbers = re.findall(r"[\d]+", text)
    return float(numbers[0]) if numbers else None

def extract_bedrooms(text: str) -> int:
    if not text:
        return None
    numbers = re.findall(r"\d+", text)
    return int(numbers[0]) if numbers else None

def scrape_aqarmap(db: Session) -> int:
    url = "https://aqarmap.com.eg/en/for-sale/apartment/cairo/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        listings = soup.select(".listing-card")

        count = 0
        if not listings:
            print("No listings found - site may require JavaScript rendering")
            print("Using Seeded data instead. Run seed.py to populate")
            return 0
        

        for listing in listings[:20]:
            try:

                title_el = listing.find("h2") or listing.find("h3")
                title = title_el.get_text(strip=True) if title_el else "Unknown"
                price_el = listing.find("data")
                price = extract_price(price_el.get_text() if price_el else "")
                location_el = listing.find(class_=re.compile("location|address", re.I))
                location = location_el.get_text(strip=True) if location_el else "Cairo"
                area_el = listing.find(class_=re.compile("rea|size|m2", re.I))
                area_m2 = extract_area(area_el.get_text() if area_el else "")
                bed_el = listing.find(class_=re.compile("bed|room", re.I))
                bedrooms = extract_bedrooms(bed_el.get_text() if bed_el else "")
                link = listing.find("a",  href=True)
                source_url = "http://aqarmap.com.eg" + link["href"] if link else None

                if source_url:
                    exits = db.query(models.Property).filter(
                        models.Property.source_url == source_url
                    ).first()
                    if exits:
                        continue

                    prop = models.Property(
                        title=title,
                        price=price,
                        area_m2=area_m2,
                        bedrooms=bedrooms,
                        location=location,
                        property_type="apartment",
                        source_url=source_url,
                        
                    )
                    db.add(prop)
                    count += 1

            except Exception as e: 
                print(f"Error parsing listing: {e}")
                continue

        db.commit()
        print(f"✅ Scraped {count} new properties")
        return count

    except Exception as e:
        print(f"❌ Scraped failed: {e}")
        raise
    
        