#!/usr/bin/env python
"""
Insert 14 laptop products for the Laptops category
"""

from models.db import products_col

laptops = [
    {
        "name": "MacBook Pro 16",
        "brand": "Apple",
        "category": "Laptops",
        "subcategory": "Laptops",
        "rent_per_day": 350.0,
        "image_url": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=600&auto=format&fit=crop&q=60",
        "description": "High-performance 16-inch MacBook Pro with M3 Pro chip",
        "specs": {
            "processor": "Apple M3 Pro",
            "ram": "18GB",
            "storage": "512GB SSD",
            "display": "16-inch Liquid Retina XDR"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Dell XPS 15",
        "brand": "Dell",
        "category": "Laptops",
        "subcategory": "Laptops",
        "rent_per_day": 320.0,
        "image_url": "https://images.unsplash.com/photo-1693206816374-c04522205b21?w=600&auto=format&fit=crop&q=60",
        "description": "Premium 15-inch ultrabook with InfinityEdge display",
        "specs": {
            "processor": "Intel Core i7",
            "ram": "16GB",
            "storage": "512GB SSD",
            "display": "15-inch FHD+ OLED"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "HP Pavilion x360",
        "brand": "HP",
        "category": "Laptops",
        "subcategory": "Laptops",
        "rent_per_day": 280.0,
        "image_url": "https://images.unsplash.com/photo-1648197395199-e7f8d3dd0a3c?w=600&auto=format&fit=crop&q=60",
        "description": "2-in-1 convertible laptop with touchscreen",
        "specs": {
            "processor": "Intel Core i5",
            "ram": "8GB",
            "storage": "256GB SSD",
            "display": "15.6-inch FHD Touch"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "ASUS VivoBook",
        "brand": "ASUS",
        "category": "Laptops",
        "subcategory": "Laptops",
        "rent_per_day": 260.0,
        "image_url": "https://images.unsplash.com/photo-1672241860863-fab879bd4a07?w=600&auto=format&fit=crop&q=60",
        "description": "Lightweight 15-inch laptop for everyday computing",
        "specs": {
            "processor": "AMD Ryzen 5",
            "ram": "8GB",
            "storage": "512GB SSD",
            "display": "15.6-inch FHD"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Lenovo ThinkPad X1",
        "brand": "Lenovo",
        "category": "Laptops",
        "subcategory": "Laptops",
        "rent_per_day": 300.0,
        "image_url": "https://images.unsplash.com/photo-1499951360447-b19be8fe80f5?w=600&auto=format&fit=crop&q=60",
        "description": "Business-class 14-inch laptop with superior keyboard",
        "specs": {
            "processor": "Intel Core i7",
            "ram": "16GB",
            "storage": "512GB SSD",
            "display": "14-inch FHD"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "MSI GS66 Stealth",
        "brand": "MSI",
        "category": "Laptops",
        "subcategory": "Laptops",
        "rent_per_day": 380.0,
        "image_url": "https://images.unsplash.com/photo-1558864559-ed673ba3610b?w=600&auto=format&fit=crop&q=60",
        "description": "Gaming laptop with RTX graphics and 240Hz display",
        "specs": {
            "processor": "Intel Core i9",
            "ram": "32GB",
            "storage": "1TB SSD",
            "display": "15.6-inch QHD 240Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Samsung Galaxy Book Pro",
        "brand": "Samsung",
        "category": "Laptops",
        "subcategory": "Laptops",
        "rent_per_day": 290.0,
        "image_url": "https://images.unsplash.com/photo-1625766763788-95dcce9bf5ac?w=600&auto=format&fit=crop&q=60",
        "description": "Ultra-thin 13.3-inch laptop with AMOLED display",
        "specs": {
            "processor": "Intel Core i7",
            "ram": "8GB",
            "storage": "512GB SSD",
            "display": "13.3-inch AMOLED"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Acer Swift 3",
        "brand": "Acer",
        "category": "Laptops",
        "subcategory": "Laptops",
        "rent_per_day": 240.0,
        "image_url": "https://images.unsplash.com/photo-1578950435899-d1c1bf932ab2?w=600&auto=format&fit=crop&q=60",
        "description": "Budget-friendly 14-inch laptop with solid performance",
        "specs": {
            "processor": "AMD Ryzen 5",
            "ram": "8GB",
            "storage": "512GB SSD",
            "display": "14-inch FHD"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "HP Spectre x360",
        "brand": "HP",
        "category": "Laptops",
        "subcategory": "Laptops",
        "rent_per_day": 340.0,
        "image_url": "https://images.unsplash.com/photo-1586077427825-15dca6b44dba?w=600&auto=format&fit=crop&q=60",
        "description": "Premium 13.5-inch convertible with stunning OLED",
        "specs": {
            "processor": "Intel Core i7",
            "ram": "16GB",
            "storage": "512GB SSD",
            "display": "13.5-inch OLED Touch"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Razer Blade 15",
        "brand": "Razer",
        "category": "Laptops",
        "subcategory": "Laptops",
        "rent_per_day": 420.0,
        "image_url": "https://images.unsplash.com/photo-1602080858428-57174f9431cf?w=600&auto=format&fit=crop&q=60",
        "description": "Ultimate gaming laptop with RTX 4080 graphics",
        "specs": {
            "processor": "Intel Core i9",
            "ram": "32GB",
            "storage": "1TB SSD",
            "display": "15.6-inch QHD 240Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Microsoft Surface Laptop 5",
        "brand": "Microsoft",
        "category": "Laptops",
        "subcategory": "Laptops",
        "rent_per_day": 310.0,
        "image_url": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=600&auto=format&fit=crop&q=60",
        "description": "Elegant 13.5-inch laptop with touchscreen",
        "specs": {
            "processor": "Intel Core i7",
            "ram": "8GB",
            "storage": "512GB SSD",
            "display": "13.5-inch Touch"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "ASUS ROG Zephyrus G14",
        "brand": "ASUS",
        "category": "Laptops",
        "subcategory": "Laptops",
        "rent_per_day": 400.0,
        "image_url": "https://images.unsplash.com/photo-1580522154071-c6ca47a859ad?w=600&auto=format&fit=crop&q=60",
        "description": "Compact gaming laptop with RTX graphics and 165Hz display",
        "specs": {
            "processor": "Intel Core i9",
            "ram": "16GB",
            "storage": "512GB SSD",
            "display": "14-inch QHD 165Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Lenovo IdeaPad Flex 5",
        "brand": "Lenovo",
        "category": "Laptops",
        "subcategory": "Laptops",
        "rent_per_day": 250.0,
        "image_url": "https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?w=600&auto=format&fit=crop&q=60",
        "description": "Versatile 14-inch 2-in-1 convertible laptop",
        "specs": {
            "processor": "AMD Ryzen 5",
            "ram": "8GB",
            "storage": "256GB SSD",
            "display": "14-inch FHD Touch"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Dell Inspiron 15",
        "brand": "Dell",
        "category": "Laptops",
        "subcategory": "Laptops",
        "rent_per_day": 220.0,
        "image_url": "https://images.unsplash.com/photo-1566647387313-9fda80664848?w=600&auto=format&fit=crop&q=60",
        "description": "Reliable 15.6-inch laptop for general computing",
        "specs": {
            "processor": "Intel Core i5",
            "ram": "8GB",
            "storage": "256GB SSD",
            "display": "15.6-inch FHD"
        },
        "availability": True,
        "reviews": []
    }
]

# Check if any laptops already exist
existing_count = products_col.count_documents({"category": "Laptops", "subcategory": "Laptops"})
if existing_count > 0:
    print(f"Warning: {existing_count} laptop products already exist. Skipping insertion.")
else:
    result = products_col.insert_many(laptops)
    inserted_ids = result.inserted_ids
    print(f"Inserted: {len(inserted_ids)} laptop products")
    for i, id in enumerate(inserted_ids, 1):
        print(f"  {i}. {id}")
