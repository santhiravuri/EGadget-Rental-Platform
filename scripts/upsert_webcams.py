from datetime import datetime
import sys, os

# Ensure project root is on sys.path so relative imports like `models` resolve
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.db import products_col

WEBCAMS = [
    {"name": "Logitech C920", "brand": "Logitech", "category": "Cameras", "subcategory": "Webcams", "tags": ["webcam","logitech"], "rent_per_day": 180.0, "image_url": "https://m.media-amazon.com/images/I/51gTkS5fHVL._AC_UY327_FMwebp_QL65_.jpg", "description": "Full HD 1080p webcam with built-in mic and USB connection.", "available": True, "created_at": datetime.utcnow()},
    {"name": "HP HD Webcam", "brand": "HP", "category": "Cameras", "subcategory": "Webcams", "tags": ["webcam","hp"], "rent_per_day": 150.0, "image_url": "https://m.media-amazon.com/images/I/61nTmIUB0LL._AC_UY327_FMwebp_QL65_.jpg", "description": "HD webcam with noise-reducing mic and plug-and-play USB.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Dell Pro Webcam", "brand": "Dell", "category": "Cameras", "subcategory": "Webcams", "tags": ["webcam","dell"], "rent_per_day": 170.0, "image_url": "https://m.media-amazon.com/images/I/71qnZFqFM9L._AC_UY327_FMwebp_QL65_.jpg", "description": "1080p webcam with wide-angle lens and USB-C adapter.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Razer Kiyo", "brand": "Razer", "category": "Cameras", "subcategory": "Webcams", "tags": ["webcam","razer"], "rent_per_day": 220.0, "image_url": "https://m.media-amazon.com/images/I/61q7GuSnqDL._AC_UY327_FMwebp_QL65_.jpg", "description": "Full HD webcam with ring light for consistent lighting.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Anker PowerConf C300", "brand": "Anker", "category": "Cameras", "subcategory": "Webcams", "tags": ["webcam","anker"], "rent_per_day": 160.0, "image_url": "https://m.media-amazon.com/images/I/71Lcx3Y2HdL._AC_UY327_FMwebp_QL65_.jpg", "description": "1080p webcam with auto-framing and dual microphones.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Microsoft LifeCam", "brand": "Microsoft", "category": "Cameras", "subcategory": "Webcams", "tags": ["webcam","microsoft"], "rent_per_day": 140.0, "image_url": "https://m.media-amazon.com/images/I/51zB4pCl8gL._AC_UY327_FMwebp_QL65_.jpg", "description": "720p/1080p webcam with noise-cancelling mic and tripod mount.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Logitech Brio 4K", "brand": "Logitech", "category": "Cameras", "subcategory": "Webcams", "tags": ["webcam","logitech"], "rent_per_day": 450.0, "image_url": "https://m.media-amazon.com/images/I/612aK9LfsSL._AC_UY327_FMwebp_QL65_.jpg", "description": "4K UHD webcam with HDR and high-quality stereo mic.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Creative Live! Cam", "brand": "Creative", "category": "Cameras", "subcategory": "Webcams", "tags": ["webcam","creative"], "rent_per_day": 130.0, "image_url": "https://images.unsplash.com/photo-1622750342107-4b60e2704157", "description": "HD webcam with built-in mic and flexible mount.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Logitech StreamCam", "brand": "Logitech", "category": "Cameras", "subcategory": "Webcams", "tags": ["webcam","logitech"], "rent_per_day": 300.0, "image_url": "https://images.unsplash.com/photo-1650017069174-341a368606a0", "description": "1080p 60fps webcam optimized for streaming and content creation.", "available": True, "created_at": datetime.utcnow()},
    {"name": "AUSDOM AW615", "brand": "AUSDOM", "category": "Cameras", "subcategory": "Webcams", "tags": ["webcam","ausdom"], "rent_per_day": 120.0, "image_url": "https://images.unsplash.com/photo-1670278458296-00ff8a63141e", "description": "Wide-angle Full HD webcam with built-in mic.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Hikvision USB Webcam", "brand": "Hikvision", "category": "Cameras", "subcategory": "Webcams", "tags": ["webcam","hikvision"], "rent_per_day": 210.0, "image_url": "https://images.unsplash.com/photo-1726127461372-547b9ffa4236", "description": "HD webcam with low-light enhancement and mic.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Logitech C505e", "brand": "Logitech", "category": "Cameras", "subcategory": "Webcams", "tags": ["webcam","logitech"], "rent_per_day": 160.0, "image_url": "https://images.unsplash.com/photo-1728971568218-03a7f87c9e99", "description": "1080p webcam with noise-reducing mic and universal mount.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Microsoft Modern Webcam", "brand": "Microsoft", "category": "Cameras", "subcategory": "Webcams", "tags": ["webcam","microsoft"], "rent_per_day": 240.0, "image_url": "https://images.unsplash.com/photo-1572534178961-a81b24c29b9d", "description": "Full HD webcam with auto-framing and dual microphones.", "available": True, "created_at": datetime.utcnow()},
    {"name": "AverMedia Live Streamer", "brand": "AverMedia", "category": "Cameras", "subcategory": "Webcams", "tags": ["webcam","avermedia"], "rent_per_day": 280.0, "image_url": "https://images.unsplash.com/photo-1636902512853-d9bc4b14a72a", "description": "High-quality webcam for streamers with good low-light performance.", "available": True, "created_at": datetime.utcnow()},
    {"name": "Logitech C925e", "brand": "Logitech", "category": "Cameras", "subcategory": "Webcams", "tags": ["webcam","logitech"], "rent_per_day": 200.0, "image_url": "https://m.media-amazon.com/images/I/71Gtq-HuQVL._AC_UY327_FMwebp_QL65_.jpg", "description": "Business-class 1080p webcam with auto light correction and stereo mic.", "available": True, "created_at": datetime.utcnow()},
]

if __name__ == '__main__':
    for p in WEBCAMS:
        filt = {"category": p["category"], "subcategory": p["subcategory"], "name": p["name"]}
        update = {"$set": p}
        res = products_col.update_one(filt, update, upsert=True)
    print(f"Processed {len(WEBCAMS)} Webcam product upserts")
