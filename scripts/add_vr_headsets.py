from datetime import datetime
from models.db import products_col

products = [
    {"name": "VR Headset 01", "brand": "Generic", "category": "Gaming Console", "subcategory": "VR Headsets", "tags": ["gaming", "vr"], "rent_per_day": 260.0, "image_url": "https://m.media-amazon.com/images/I/61Y5E9xTa5L._AC_UY327_FMwebp_QL65_.jpg", "available": True, "created_at": datetime.utcnow()},
    {"name": "VR Headset 02", "brand": "Generic", "category": "Gaming Console", "subcategory": "VR Headsets", "tags": ["gaming", "vr"], "rent_per_day": 270.0, "image_url": "https://m.media-amazon.com/images/I/61Gw3WPuq1L._AC_UY327_FMwebp_QL65_.jpg", "available": True, "created_at": datetime.utcnow()},
    {"name": "VR Headset 03", "brand": "Generic", "category": "Gaming Console", "subcategory": "VR Headsets", "tags": ["gaming", "vr"], "rent_per_day": 280.0, "image_url": "https://m.media-amazon.com/images/I/51Ag5K4YUpL._AC_UL480_FMwebp_QL65_.jpg", "available": True, "created_at": datetime.utcnow()},
    {"name": "VR Headset 04", "brand": "Generic", "category": "Gaming Console", "subcategory": "VR Headsets", "tags": ["gaming", "vr"], "rent_per_day": 290.0, "image_url": "https://m.media-amazon.com/images/I/51YyPYbP-wL._AC_UY327_FMwebp_QL65_.jpg", "available": True, "created_at": datetime.utcnow()},
    {"name": "VR Headset 05", "brand": "Generic", "category": "Gaming Console", "subcategory": "VR Headsets", "tags": ["gaming", "vr"], "rent_per_day": 300.0, "image_url": "https://m.media-amazon.com/images/I/51wmsuPdQcL._AC_UY327_FMwebp_QL65_.jpg", "available": True, "created_at": datetime.utcnow()},
    {"name": "VR Headset 06", "brand": "Generic", "category": "Gaming Console", "subcategory": "VR Headsets", "tags": ["gaming", "vr"], "rent_per_day": 310.0, "image_url": "https://m.media-amazon.com/images/I/51P5eFylJJL._AC_UY327_FMwebp_QL65_.jpg", "available": True, "created_at": datetime.utcnow()},
    {"name": "VR Headset 07", "brand": "Generic", "category": "Gaming Console", "subcategory": "VR Headsets", "tags": ["gaming", "vr"], "rent_per_day": 320.0, "image_url": "https://m.media-amazon.com/images/I/61Eg0zsASiL._AC_UY327_FMwebp_QL65_.jpg", "available": True, "created_at": datetime.utcnow()},
    {"name": "VR Headset 08", "brand": "Generic", "category": "Gaming Console", "subcategory": "VR Headsets", "tags": ["gaming", "vr"], "rent_per_day": 330.0, "image_url": "https://m.media-amazon.com/images/I/61-tgcn-R3L._AC_UY327_FMwebp_QL65_.jpg", "available": True, "created_at": datetime.utcnow()},
    {"name": "VR Headset 09", "brand": "Generic", "category": "Gaming Console", "subcategory": "VR Headsets", "tags": ["gaming", "vr"], "rent_per_day": 340.0, "image_url": "https://m.media-amazon.com/images/I/61Y5E9xTa5L._AC_UY327_FMwebp_QL65_.jpg", "available": True, "created_at": datetime.utcnow()},
    {"name": "VR Headset 10", "brand": "Generic", "category": "Gaming Console", "subcategory": "VR Headsets", "tags": ["gaming", "vr"], "rent_per_day": 350.0, "image_url": "https://m.media-amazon.com/images/I/61oMxkcJWlL._AC_UY327_FMwebp_QL65_.jpg", "available": True, "created_at": datetime.utcnow()},
    {"name": "VR Headset 11", "brand": "Generic", "category": "Gaming Console", "subcategory": "VR Headsets", "tags": ["gaming", "vr"], "rent_per_day": 360.0, "image_url": "https://m.media-amazon.com/images/I/51Ag5K4YUpL._AC_UY327_FMwebp_QL65_.jpg", "available": True, "created_at": datetime.utcnow()},
    {"name": "VR Headset 12", "brand": "Generic", "category": "Gaming Console", "subcategory": "VR Headsets", "tags": ["gaming", "vr"], "rent_per_day": 370.0, "image_url": "https://m.media-amazon.com/images/I/41qprA--3-L._AC_UY327_FMwebp_QL65_.jpg", "available": True, "created_at": datetime.utcnow()},
    {"name": "VR Headset 13", "brand": "Generic", "category": "Gaming Console", "subcategory": "VR Headsets", "tags": ["gaming", "vr"], "rent_per_day": 380.0, "image_url": "https://m.media-amazon.com/images/I/51AQetEt-qL._AC_UL480_FMwebp_QL65_.jpg", "available": True, "created_at": datetime.utcnow()},
    {"name": "VR Headset 14", "brand": "Generic", "category": "Gaming Console", "subcategory": "VR Headsets", "tags": ["gaming", "vr"], "rent_per_day": 390.0, "image_url": "https://m.media-amazon.com/images/I/61nkctF66PL._AC_UY327_FMwebp_QL65_.jpg", "available": True, "created_at": datetime.utcnow()},
    {"name": "VR Headset 15", "brand": "Generic", "category": "Gaming Console", "subcategory": "VR Headsets", "tags": ["gaming", "vr"], "rent_per_day": 400.0, "image_url": "https://m.media-amazon.com/images/I/61Gw3WPuq1L._AC_UY327_FMwebp_QL65_.jpg", "available": True, "created_at": datetime.utcnow()},
    {"name": "VR Headset 16", "brand": "Generic", "category": "Gaming Console", "subcategory": "VR Headsets", "tags": ["gaming", "vr"], "rent_per_day": 410.0, "image_url": "https://m.media-amazon.com/images/I/41qGZbEOP5L._AC_UY327_FMwebp_QL65_.jpg", "available": True, "created_at": datetime.utcnow()},
]

def run():
    added = 0
    for p in products:
        res = products_col.update_one({"name": p["name"]}, {"$setOnInsert": p}, upsert=True)
        if res.upserted_id:
            added += 1
    print(f"Added {added} VR Headsets." if added else "No new VR Headsets added.")

if __name__ == "__main__":
    run()
