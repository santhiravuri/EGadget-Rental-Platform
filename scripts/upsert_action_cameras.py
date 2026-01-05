from datetime import datetime
import sys, os

# Ensure project root is on sys.path so relative imports like `models` resolve
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.db import products_col

ACTION_CAMERAS = [
    {"name": "GoPro Hero 11", "brand": "GoPro", "category": "Cameras", "subcategory": "Action Cameras", "tags": ["action", "gopro"], "rent_per_day": 900.0, "image_url": "https://m.media-amazon.com/images/I/81a3pm3nxsL._AC_UY327_FMwebp_QL65_.jpg", "description": "GoPro Hero 11 — rugged action camera for adventures.", "available": True, "created_at": datetime.utcnow()},
    {"name": "DJI Action 4", "brand": "DJI", "category": "Cameras", "subcategory": "Action Cameras", "tags": ["action", "dji"], "rent_per_day": 1000.0, "image_url": "https://m.media-amazon.com/images/I/61TnLqxUbeL._AC_UY327_FMwebp_QL65_.jpg", "description": "DJI Action 4 — stabilized action camera for dynamic shooting.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Insta360 X3", "brand": "Insta360", "category": "Cameras", "subcategory": "Action Cameras", "tags": ["action", "insta360"], "rent_per_day": 950.0, "image_url": "https://m.media-amazon.com/images/I/610NQUzk2xL._AC_UY327_FMwebp_QL65_.jpg", "description": "Insta360 X3 — 360-degree action camera for immersive shots.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Akaso V50 Pro", "brand": "Akaso", "category": "Cameras", "subcategory": "Action Cameras", "tags": ["action", "akaso"], "rent_per_day": 250.0, "image_url": "https://m.media-amazon.com/images/I/71wlB2kVc+L._AC_UY327_FMwebp_QL65_.jpg", "description": "Akaso V50 Pro — budget-friendly action camera with 4K.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Sony RX0 II", "brand": "Sony", "category": "Cameras", "subcategory": "Action Cameras", "tags": ["action", "sony"], "rent_per_day": 1200.0, "image_url": "https://m.media-amazon.com/images/I/61126QGucML._AC_UY327_FMwebp_QL65_.jpg", "description": "Sony RX0 II — compact, rugged action camera with pro features.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Garmin VIRB Ultra 30", "brand": "Garmin", "category": "Cameras", "subcategory": "Action Cameras", "tags": ["action", "garmin"], "rent_per_day": 700.0, "image_url": "https://m.media-amazon.com/images/I/710PE68NEcL._AC_UL960_FMwebp_QL65_.jpg", "description": "Garmin VIRB Ultra 30 — GPS-enabled action camera.", "available": True, "created_at": datetime.utcnow()},
    {"name": "GoPro Hero 10", "brand": "GoPro", "category": "Cameras", "subcategory": "Action Cameras", "tags": ["action", "gopro"], "rent_per_day": 800.0, "image_url": "https://m.media-amazon.com/images/I/71FdBD3y0rL._AC_UY327_FMwebp_QL65_.jpg", "description": "GoPro Hero 10 — high frame rate action camera.", "available": True, "created_at": datetime.utcnow()},
    {"name": "DJI Osmo Action", "brand": "DJI", "category": "Cameras", "subcategory": "Action Cameras", "tags": ["action", "dji"], "rent_per_day": 850.0, "image_url": "https://m.media-amazon.com/images/I/611MFpyilLL._AC_UY327_FMwebp_QL65_.jpg", "description": "DJI Osmo Action — dual-screen action camera for creators.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Ricoh WG-M2", "brand": "Ricoh", "category": "Cameras", "subcategory": "Action Cameras", "tags": ["action", "ricoh"], "rent_per_day": 400.0, "image_url": "https://m.media-amazon.com/images/I/61Md360e+kL._AC_UY327_FMwebp_QL65_.jpg", "description": "Ricoh WG-M2 — rugged action cam for sporty use.", "available": True, "created_at": datetime.utcnow()},
    {"name": "SJCAM SJ8 Pro", "brand": "SJCAM", "category": "Cameras", "subcategory": "Action Cameras", "tags": ["action", "sjcam"], "rent_per_day": 300.0, "image_url": "https://m.media-amazon.com/images/I/61TnLqxUbeL._AC_UY327_FMwebp_QL65_.jpg", "description": "SJCAM SJ8 Pro — value action camera with 4K capability.", "available": True, "created_at": datetime.utcnow()},
    {"name": "GoPro MAX", "brand": "GoPro", "category": "Cameras", "subcategory": "Action Cameras", "tags": ["action", "gopro", "360"], "rent_per_day": 1100.0, "image_url": "https://images.unsplash.com/photo-1605661450842-f040d84f3680?w=600&auto=format&fit=crop&q=60", "description": "GoPro MAX — 360-degree action camera for immersive capture.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Insta360 One R", "brand": "Insta360", "category": "Cameras", "subcategory": "Action Cameras", "tags": ["action", "insta360"], "rent_per_day": 950.0, "image_url": "https://images.unsplash.com/photo-1752080195669-1bd8407ead9f?w=600&auto=format&fit=crop&q=60", "description": "Insta360 One R — modular action camera system.", "available": True, "created_at": datetime.utcnow()},
    {"name": "ThiEYE T5 Edge", "brand": "ThiEYE", "category": "Cameras", "subcategory": "Action Cameras", "tags": ["action", "thieye"], "rent_per_day": 220.0, "image_url": "https://images.unsplash.com/photo-1654197308647-e10569aa987a?w=600&auto=format&fit=crop&q=60", "description": "ThiEYE T5 Edge — compact action cam with stabilization.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Akaso Brave 8", "brand": "Akaso", "category": "Cameras", "subcategory": "Action Cameras", "tags": ["action", "akaso"], "rent_per_day": 260.0, "image_url": "https://images.unsplash.com/photo-1559645147-bbd3634fcd8f?w=600&auto=format&fit=crop&q=60", "description": "Akaso Brave 8 — lightweight action camera for adventures.", "available": True, "created_at": datetime.utcnow()},
    {"name": "RunCam 5", "brand": "RunCam", "category": "Cameras", "subcategory": "Action Cameras", "tags": ["action", "runcam"], "rent_per_day": 480.0, "image_url": "https://images.unsplash.com/photo-1690977678689-dc0060822e7e?w=600&auto=format&fit=crop&q=60", "description": "RunCam 5 — action camera optimized for drone and action sports.", "available": True, "created_at": datetime.utcnow()},
]

if __name__ == '__main__':
    for p in ACTION_CAMERAS:
        filt = {"category": p["category"], "subcategory": p["subcategory"], "name": p["name"]}
        update = {"$set": p}
        res = products_col.update_one(filt, update, upsert=True)
    print(f"Processed {len(ACTION_CAMERAS)} Action Camera product upserts")
