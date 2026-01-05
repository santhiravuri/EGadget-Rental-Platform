from datetime import datetime
import sys, os

# Ensure project root is on sys.path so relative imports like `models` resolve
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.db import products_col

DRONES = [
    {"name": "DJI Mini 2", "brand": "DJI", "category": "Cameras", "subcategory": "Drones", "rent_per_day": 2000.0, "image_url": "https://m.media-amazon.com/images/I/51Z2XtPb+dL._AC_UL480_FMwebp_QL65_.jpg", "description": "Compact lightweight drone with 4K video and 31-min flight time.", "available": True, "created_at": datetime.utcnow()},
    {"name": "DJI Air 2S", "brand": "DJI", "category": "Cameras", "subcategory": "Drones", "rent_per_day": 3000.0, "image_url": "https://m.media-amazon.com/images/I/71KcEChYZUL._AC_UL480_FMwebp_QL65_.jpg", "description": "Professional drone with 1-inch sensor and intelligent flight modes.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Autel EVO Lite", "brand": "Autel", "category": "Cameras", "subcategory": "Drones", "rent_per_day": 2800.0, "image_url": "https://m.media-amazon.com/images/I/610sk349iLL._AC_UL480_FMwebp_QL65_.jpg", "description": "High-performance drone with excellent low-light imaging.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Parrot Anafi", "brand": "Parrot", "category": "Cameras", "subcategory": "Drones", "rent_per_day": 1500.0, "image_url": "https://m.media-amazon.com/images/I/61OMf3CSP5L._AC_UL480_FMwebp_QL65_.jpg", "description": "Lightweight 4K drone with tilt gimbal and portable design.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Holy Stone HS720", "brand": "Holy Stone", "category": "Cameras", "subcategory": "Drones", "rent_per_day": 1200.0, "image_url": "https://m.media-amazon.com/images/I/713ie-iOZXL._AC_UL480_FMwebp_QL65_.jpg", "description": "Durable GPS drone with 4K camera for hobbyists.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Potensic Dreamer", "brand": "Potensic", "category": "Cameras", "subcategory": "Drones", "rent_per_day": 1100.0, "image_url": "https://m.media-amazon.com/images/I/61F9ECubiuL._AC_UL480_FMwebp_QL65_.jpg", "description": "Stable 2.7K camera drone with follow-me and waypoint modes.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Hubsan Zino", "brand": "Hubsan", "category": "Cameras", "subcategory": "Drones", "rent_per_day": 1300.0, "image_url": "https://m.media-amazon.com/images/I/71HvJJttgOL._AC_UL480_FMwebp_QL65_.jpg", "description": "Compact 4K drone with GPS and intelligent flight features.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Ryze Tello", "brand": "Ryze", "category": "Cameras", "subcategory": "Drones", "rent_per_day": 700.0, "image_url": "https://m.media-amazon.com/images/I/61KZ3pluB7L._AC_UL480_FMwebp_QL65_.jpg", "description": "Lightweight programmable drone ideal for beginners and education.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Skydio 2", "brand": "Skydio", "category": "Cameras", "subcategory": "Drones", "rent_per_day": 3500.0, "image_url": "https://m.media-amazon.com/images/I/71tEhwDqjJL._AC_UL480_FMwebp_QL65_.jpg", "description": "Autonomous obstacle-avoiding drone for advanced cinematography.", "available": True, "created_at": datetime.utcnow()},
    {"name": "SkyPro Explorer", "brand": "SkyPro", "category": "Cameras", "subcategory": "Drones", "rent_per_day": 900.0, "image_url": "https://images.unsplash.com/photo-1521405924368-64c5b84bec60?w=600&auto=format&fit=crop&q=60", "description": "Affordable 1080p drone with stable flight and easy controls.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Air Vision Mini", "brand": "AirVision", "category": "Cameras", "subcategory": "Drones", "rent_per_day": 850.0, "image_url": "https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=600&auto=format&fit=crop&q=60", "description": "Pocket-sized drone for quick aerial shots and practice flights.", "available": True, "created_at": datetime.utcnow()},
    {"name": "FlyCam Pro", "brand": "FlyCam", "category": "Cameras", "subcategory": "Drones", "rent_per_day": 1400.0, "image_url": "https://images.unsplash.com/photo-1579829366248-204fe8413f31?w=600&auto=format&fit=crop&q=60", "description": "Reliable 2.7K drone with intelligent return-to-home.", "available": True, "created_at": datetime.utcnow()},
    {"name": "AeroShot 4K", "brand": "AeroShot", "category": "Cameras", "subcategory": "Drones", "rent_per_day": 2400.0, "image_url": "https://images.unsplash.com/photo-1456615913800-c33540eac399?w=600&auto=format&fit=crop&q=60", "description": "4K-capable drone for semi-professional aerial videography.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Nimbus Scout", "brand": "Nimbus", "category": "Cameras", "subcategory": "Drones", "rent_per_day": 1000.0, "image_url": "https://images.unsplash.com/photo-1514505213055-b456c4420f67?w=600&auto=format&fit=crop&q=60", "description": "Easy-to-fly quadcopter with steady camera and good battery life.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Orbit Ranger", "brand": "Orbit", "category": "Cameras", "subcategory": "Drones", "rent_per_day": 1600.0, "image_url": "https://images.unsplash.com/photo-1679301641273-5dc4cb00edaa?w=600&auto=format&fit=crop&q=60", "description": "Versatile drone with multiple flight modes for creative shots.", "available": True, "created_at": datetime.utcnow()},
]

if __name__ == '__main__':
    for p in DRONES:
        filt = {"category": p["category"], "subcategory": p["subcategory"], "name": p["name"]}
        update = {"$set": p}
        products_col.update_one(filt, update, upsert=True)
    print(f"Processed {len(DRONES)} Drone product upserts")
