"""Insert 9 smartphone products into the DB (Mobiles -> Smartphones)
Run: python add_smartphones_full.py
"""
from datetime import datetime
from models.db import products_col

phones = [
    {
        "name": "iPhone 14 Pro",
        "brand": "Apple",
        "category": "Mobiles",
        "subcategory": "Smartphones",
        "rent_per_day": 1300.0,
        "image_url": "https://images.pexels.com/photos/607812/pexels-photo-607812.jpeg",
        "short_description": "Pro performance and cinematic photography.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
    {
        "name": "Galaxy S23 Ultra",
        "brand": "Samsung",
        "category": "Mobiles",
        "subcategory": "Smartphones",
        "rent_per_day": 1350.0,
        "image_url": "https://images.pexels.com/photos/6632995/pexels-photo-6632995.jpeg",
        "short_description": "Flagship camera system and long battery life.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
    {
        "name": "Pixel 8 Pro",
        "brand": "Google",
        "category": "Mobiles",
        "subcategory": "Smartphones",
        "rent_per_day": 1150.0,
        "image_url": "https://images.pexels.com/photos/8487808/pexels-photo-8487808.jpeg",
        "short_description": "Clean Android with top-tier computational photography.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
    {
        "name": "OnePlus 12 Pro",
        "brand": "OnePlus",
        "category": "Mobiles",
        "subcategory": "Smartphones",
        "rent_per_day": 1050.0,
        "image_url": "https://images.pexels.com/photos/1092644/pexels-photo-1092644.jpeg",
        "short_description": "Ultra-fast charging and smooth experience.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
    {
        "name": "Samsung Galaxy S23",
        "brand": "Samsung",
        "category": "Mobiles",
        "subcategory": "Smartphones",
        "rent_per_day": 1100.0,
        "image_url": "https://plus.unsplash.com/premium_photo-1680985551022-ad298e8a5f82?w=600&auto=format&fit=crop&q=60",
        "short_description": "Popular flagship with balanced performance.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
    {
        "name": "iPhone 14",
        "brand": "Apple",
        "category": "Mobiles",
        "subcategory": "Smartphones",
        "rent_per_day": 1200.0,
        "image_url": "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg",
        "short_description": "Reliable performance and great ecosystem integration.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
    {
        "name": "Pixel 7",
        "brand": "Google",
        "category": "Mobiles",
        "subcategory": "Smartphones",
        "rent_per_day": 950.0,
        "image_url": "https://images.pexels.com/photos/404280/pexels-photo-404280.jpeg",
        "short_description": "Great value with excellent camera features.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
    {
        "name": "Moto G Power",
        "brand": "Motorola",
        "category": "Mobiles",
        "subcategory": "Smartphones",
        "rent_per_day": 450.0,
        "image_url": "https://images.pexels.com/photos/1786433/pexels-photo-1786433.jpeg",
        "short_description": "Budget phone with long battery life.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
    {
        "name": "Nokia X20",
        "brand": "Nokia",
        "category": "Mobiles",
        "subcategory": "Smartphones",
        "rent_per_day": 500.0,
        "image_url": "https://images.pexels.com/photos/47261/pexels-photo-47261.jpeg",
        "short_description": "Durable build and clean software.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
]

inserted = []
for p in phones:
    q = {"name": p["name"], "category": p["category"], "subcategory": p["subcategory"]}
    existing = products_col.find_one(q)
    if existing:
        print(f"Exists: {p['name']} (skipping)")
    else:
        res = products_col.insert_one(p)
        inserted.append(str(res.inserted_id))
        print(f"Inserted: {p['name']} -> {res.inserted_id}")

print('\nInserted IDs:')
for i in inserted:
    print(' -', i)
