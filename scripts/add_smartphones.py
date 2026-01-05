"""Add/ensure smartphone products in the database for Mobiles -> Smartphones
Run: python add_smartphones.py
"""
from datetime import datetime
from models.db import products_col

smartphones = [
    {
        "name": "Samsung Galaxy S23",
        "brand": "Samsung",
        "category": "Mobiles",
        "subcategory": "Smartphones",
        "rent_per_day": 1100.0,
        "image_url": "https://images.unsplash.com/photo-1584006682522-dc17d6c0d9ac?w=600&auto=format&fit=crop&q=60",
        "short_description": "Powerful flagship with excellent camera and smooth performance.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
    {
        "name": "Apple iPhone 14",
        "brand": "Apple",
        "category": "Mobiles",
        "subcategory": "Smartphones",
        "rent_per_day": 1200.0,
        "image_url": "https://images.unsplash.com/photo-1672413514634-4781b15fd89e?w=600&auto=format&fit=crop&q=60",
        "short_description": "Sleek design and reliable performance with iOS ecosystem.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
    {
        "name": "Google Pixel 8",
        "brand": "Google",
        "category": "Mobiles",
        "subcategory": "Smartphones",
        "rent_per_day": 1050.0,
        "image_url": "https://images.unsplash.com/photo-1719945421298-f03d3d80c3e1?w=600&auto=format&fit=crop&q=60",
        "short_description": "Stock Android experience with best-in-class computational photography.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
    {
        "name": "OnePlus 12",
        "brand": "OnePlus",
        "category": "Mobiles",
        "subcategory": "Smartphones",
        "rent_per_day": 950.0,
        "image_url": "https://images.unsplash.com/photo-1621330396167-b3d451b9b83b?w=600&auto=format&fit=crop&q=60",
        "short_description": "Fast charging and smooth performance for power users.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
]

inserted = []
for sp in smartphones:
    # use a combination of name + category + subcategory to detect duplicates
    q = {"name": sp["name"], "category": sp["category"], "subcategory": sp["subcategory"]}
    existing = products_col.find_one(q)
    if existing:
        print(f"Exists: {sp['name']} (skipping)")
    else:
        res = products_col.insert_one(sp)
        inserted.append(str(res.inserted_id))
        print(f"Inserted: {sp['name']} -> {res.inserted_id}")

print("\nDone. Inserted IDs:")
for _id in inserted:
    print(" - ", _id)
