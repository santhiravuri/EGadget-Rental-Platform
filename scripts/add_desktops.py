#!/usr/bin/env python
"""
Insert 15 desktop products for the Laptops > Desktops subcategory
"""

from models.db import products_col

desktops = [
    {
        "name": "Dell OptiPlex 7090 Tower",
        "brand": "Dell",
        "category": "Laptops",
        "subcategory": "Desktops",
        "rent_per_day": 180.0,
        "image_url": "https://plus.unsplash.com/premium_photo-1681816189679-fa02d1acd1de?w=600&auto=format&fit=crop&q=60",
        "description": "Professional tower PC with Intel Core i7 and 16GB RAM",
        "specs": {
            "processor": "Intel Core i7-11700",
            "ram": "16GB DDR4",
            "storage": "512GB SSD",
            "form_factor": "Tower"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Apple iMac 24-inch M3",
        "brand": "Apple",
        "category": "Laptops",
        "subcategory": "Desktops",
        "rent_per_day": 280.0,
        "image_url": "https://plus.unsplash.com/premium_photo-1683436791486-508249532f52?w=600&auto=format&fit=crop&q=60",
        "description": "All-in-one iMac with stunning Retina display and M3 chip",
        "specs": {
            "processor": "Apple M3",
            "ram": "8GB unified memory",
            "storage": "256GB SSD",
            "display": "24-inch Retina 4.5K"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "HP Pavilion Desktop TP01",
        "brand": "HP",
        "category": "Laptops",
        "subcategory": "Desktops",
        "rent_per_day": 160.0,
        "image_url": "https://images.unsplash.com/photo-1708200216314-455e3487392a?w=600&auto=format&fit=crop&q=60",
        "description": "Home and office desktop with AMD Ryzen processor",
        "specs": {
            "processor": "AMD Ryzen 5 5600G",
            "ram": "8GB DDR4",
            "storage": "256GB SSD",
            "form_factor": "Mini Tower"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "ASUS VivoPC X1 Compact",
        "brand": "ASUS",
        "category": "Laptops",
        "subcategory": "Desktops",
        "rent_per_day": 140.0,
        "image_url": "https://images.unsplash.com/photo-1755436613059-6ebdd563bb73?w=600&auto=format&fit=crop&q=60",
        "description": "Compact desktop perfect for small spaces and offices",
        "specs": {
            "processor": "Intel Core i5-10400",
            "ram": "8GB DDR4",
            "storage": "512GB SSD",
            "form_factor": "Ultra-compact"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Corsair Vengeance i7200",
        "brand": "Corsair",
        "category": "Laptops",
        "subcategory": "Desktops",
        "rent_per_day": 220.0,
        "image_url": "https://images.unsplash.com/photo-1636485043041-e1d05b9f0662?w=600&auto=format&fit=crop&q=60",
        "description": "Gaming desktop with RTX 4060 graphics and RGB lighting",
        "specs": {
            "processor": "Intel Core i7-12700",
            "gpu": "NVIDIA RTX 4060",
            "ram": "16GB DDR5",
            "storage": "1TB NVMe SSD"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "MSI Infinite B590",
        "brand": "MSI",
        "category": "Laptops",
        "subcategory": "Desktops",
        "rent_per_day": 200.0,
        "image_url": "https://images.unsplash.com/photo-1639730992634-d048fe1dfdaf?w=600&auto=format&fit=crop&q=60",
        "description": "Performance desktop for gaming and content creation",
        "specs": {
            "processor": "Intel Core i7-12700K",
            "gpu": "NVIDIA RTX 4070",
            "ram": "32GB DDR5",
            "storage": "1TB NVMe SSD"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Lenovo ThinkCentre M90",
        "brand": "Lenovo",
        "category": "Laptops",
        "subcategory": "Desktops",
        "rent_per_day": 150.0,
        "image_url": "https://images.unsplash.com/photo-1658857735566-784ae5c04f90?w=600&auto=format&fit=crop&q=60",
        "description": "Business desktop with Intel Core i5 and 8GB RAM",
        "specs": {
            "processor": "Intel Core i5-11400",
            "ram": "8GB DDR4",
            "storage": "512GB SSD",
            "form_factor": "SFF Tower"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "NZXT BLD Streaming PC",
        "brand": "NZXT",
        "category": "Laptops",
        "subcategory": "Desktops",
        "rent_per_day": 240.0,
        "image_url": "https://images.unsplash.com/photo-1638857367146-cec84948c8aa?w=600&auto=format&fit=crop&q=60",
        "description": "Streaming optimized PC with excellent thermal design",
        "specs": {
            "processor": "Intel Core i9-12900K",
            "gpu": "NVIDIA RTX 4090",
            "ram": "32GB DDR5",
            "storage": "2TB NVMe SSD"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Alienware Aurora R13",
        "brand": "Alienware",
        "category": "Laptops",
        "subcategory": "Desktops",
        "rent_per_day": 300.0,
        "image_url": "https://images.unsplash.com/photo-1609769855973-b3208b494dfd?w=600&auto=format&fit=crop&q=60",
        "description": "Premium gaming desktop with top-tier components",
        "specs": {
            "processor": "Intel Core i9-12900KS",
            "gpu": "NVIDIA RTX 4090",
            "ram": "64GB DDR5",
            "storage": "4TB NVMe SSD"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "ASUS ROG Strix G10CE",
        "brand": "ASUS",
        "category": "Laptops",
        "subcategory": "Desktops",
        "rent_per_day": 260.0,
        "image_url": "https://m.media-amazon.com/images/I/71sLEcELGNL._AC_UY327_FMwebp_QL65_.jpg",
        "description": "Gaming tower with RTX 4080 and customizable RGB lighting",
        "specs": {
            "processor": "Intel Core i9-12700KF",
            "gpu": "NVIDIA RTX 4080",
            "ram": "32GB DDR5",
            "storage": "1TB NVMe SSD"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Razer Tomahawk Gaming PC",
        "brand": "Razer",
        "category": "Laptops",
        "subcategory": "Desktops",
        "rent_per_day": 290.0,
        "image_url": "https://m.media-amazon.com/images/I/71kq1LpXmAL._AC_UY327_FMwebp_QL65_.jpg",
        "description": "Premium gaming machine with Razer chroma integration",
        "specs": {
            "processor": "Intel Core i9-12900KS",
            "gpu": "NVIDIA RTX 4090",
            "ram": "48GB DDR5",
            "storage": "2TB NVMe SSD"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Acer Aspire XC-1760",
        "brand": "Acer",
        "category": "Laptops",
        "subcategory": "Desktops",
        "rent_per_day": 130.0,
        "image_url": "https://m.media-amazon.com/images/I/614OHqM5U-L._AC_UY327_FMwebp_QL65_.jpg",
        "description": "Entry-level desktop with AMD Ryzen 5 processor",
        "specs": {
            "processor": "AMD Ryzen 5 5500",
            "ram": "8GB DDR4",
            "storage": "256GB SSD",
            "form_factor": "Mini Tower"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Gigabyte G5 GD65",
        "brand": "Gigabyte",
        "category": "Laptops",
        "subcategory": "Desktops",
        "rent_per_day": 210.0,
        "image_url": "https://m.media-amazon.com/images/I/61broXFs0VL._AC_UY327_FMwebp_QL65_.jpg",
        "description": "High-performance gaming desktop with liquid cooling",
        "specs": {
            "processor": "Intel Core i7-12700",
            "gpu": "NVIDIA RTX 4070 Ti",
            "ram": "32GB DDR5",
            "storage": "1TB NVMe SSD"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Skytech Prism II",
        "brand": "Skytech",
        "category": "Laptops",
        "subcategory": "Desktops",
        "rent_per_day": 190.0,
        "image_url": "https://m.media-amazon.com/images/I/71h8h2G+bXL._AC_UY327_FMwebp_QL65_.jpg",
        "description": "Budget gaming desktop with RTX 3060 graphics",
        "specs": {
            "processor": "Intel Core i5-12400",
            "gpu": "NVIDIA RTX 3060",
            "ram": "16GB DDR4",
            "storage": "500GB SSD"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "iBuyPower Slate 5MR",
        "brand": "iBuyPower",
        "category": "Laptops",
        "subcategory": "Desktops",
        "rent_per_day": 170.0,
        "image_url": "https://tse4.mm.bing.net/th/id/OIP.mGCM6NWay7Emj-26nJ8TmgHaE8?pid=Api&P=0&h=180",
        "description": "Mid-range gaming desktop with solid performance",
        "specs": {
            "processor": "Intel Core i7-12700",
            "gpu": "NVIDIA RTX 4060 Ti",
            "ram": "16GB DDR5",
            "storage": "512GB NVMe SSD"
        },
        "availability": True,
        "reviews": []
    }
]

# Check if any desktops already exist
existing_count = products_col.count_documents({"category": "Laptops", "subcategory": "Desktops"})
if existing_count > 0:
    print(f"Warning: {existing_count} desktop products already exist. Skipping insertion.")
else:
    result = products_col.insert_many(desktops)
    inserted_ids = result.inserted_ids
    print(f"Inserted: {len(inserted_ids)} desktop products")
    for i, id in enumerate(inserted_ids, 1):
        print(f"  {i}. {id}")
