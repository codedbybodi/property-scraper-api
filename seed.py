from db import SessionLocal
import models

def seed():
    db =  SessionLocal()

    properties = [
        {"title": "Creekview by Mountain view", "price": 5400000, "area_m2": 80, "bedrooms": 1, "location" : "New Cairo"},
        {"title": "Creekview by Mountain view", "price": 6900000, "area_m2": 125, "bedrooms": 2, "location" : "New Cairo"},
        {"title": "Creekview by Mountain view", "price": 8600000, "area_m2": 155, "bedrooms": 3, "location" : "New Cairo"},
        {"title": "Sumou Blvd by Paragon Adeer", "price": 4800000, "area_m2": 95, "bedrooms": 1, "location" : "Mostakbal City"},
        {"title": "Sumou Blvd by Paragon Adeer", "price": 7600000, "area_m2": 129, "bedrooms": 2, "location" : "Mostakbal City"},
        {"title": "Sumou Blvd by Paragon Adeer", "price": 12000000, "area_m2": 194, "bedrooms": 3, "location" : "Mostakbal City"},
        {"title": "East vale by SODIC", "price": 12273040, "area_m2": 81, "bedrooms": 1, "location" : "Mostakbal City"},
        {"title": "East vale by SODIC", "price": 17457440, "area_m2": 121, "bedrooms": 2, "location" : "Mostakbal City"},
        {"title": "East vale by SODIC", "price": 18877040, "area_m2": 181, "bedrooms": 3, "location" : "Mostakbal City"},
        {"title": "Hyde Park", "price": 7419500, "area_m2": 73, "bedrooms": 1, "location" : "New Cairo"},
        {"title": "Hyde Park", "price": 16660000, "area_m2": 123, "bedrooms": 3, "location" : "New Cairo"},
        {"title": "Hyde Park", "price": 19690000, "area_m2": 161, "bedrooms": 3, "location" : "New Cairo"},
        {"title": "Palm Hills", "price": 9584000, "area_m2": 70, "bedrooms": 1, "location" : "New Cairo"},
        {"title": "Palm Hills", "price": 10700000, "area_m2": 149, "bedrooms": 2, "location" : "New Cairo"},
        {"title": "Palm Hills", "price": 27077000, "area_m2": 220, "bedrooms": 3, "location" : "New Cairo"},
    ]

    for p in properties:
        exists = db.query(models.Property).filter(
            models.Property.title == p["title"]
        ).first()
        if not exists:
            db.add(models.Property(**p))


    db.commit()
    db.close()
    print(f" Seeded {len(properties)} properties!")

if __name__ == "__main__":
    seed()

