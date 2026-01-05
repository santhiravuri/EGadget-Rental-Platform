#!/usr/bin/env python
"""
Insert 12 gaming laptop products for the Laptops > Gaming Laptops subcategory
"""

from models.db import products_col

gaming_laptops = [
    {
        "name": "ASUS ROG Strix G16",
        "brand": "ASUS",
        "category": "Laptops",
        "subcategory": "Gaming Laptops",
        "rent_per_day": 450.0,
        "image_url": "https://m.media-amazon.com/images/I/71X+a0NItZL._AC_UY327_FMwebp_QL65_.jpg",
        "description": "High-performance gaming laptop with RTX 4090 and 165Hz display",
        "specs": {
            "processor": "Intel Core i9-13th Gen",
            "gpu": "NVIDIA RTX 4090",
            "ram": "32GB DDR5",
            "storage": "1TB NVMe SSD",
            "display": "16-inch QHD+ 240Hz",
            "refresh_rate": "240Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "MSI Raider GE78",
        "brand": "MSI",
        "category": "Laptops",
        "subcategory": "Gaming Laptops",
        "rent_per_day": 480.0,
        "image_url": "https://m.media-amazon.com/images/I/71Te7LU5GOL._AC_UY327_FMwebp_QL65_.jpg",
        "description": "Ultimate gaming powerhouse with RTX 4090 and 240Hz panel",
        "specs": {
            "processor": "Intel Core i9-13th Gen",
            "gpu": "NVIDIA RTX 4090",
            "ram": "32GB DDR5",
            "storage": "1TB SSD",
            "display": "17-inch QHD 240Hz",
            "refresh_rate": "240Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Acer Predator Triton",
        "brand": "Acer",
        "category": "Laptops",
        "subcategory": "Gaming Laptops",
        "rent_per_day": 420.0,
        "image_url": "https://m.media-amazon.com/images/I/81DPEz2+8yL._AC_UY327_FMwebp_QL65_.jpg",
        "description": "Premium gaming laptop with RTX 4080 and 240Hz display",
        "specs": {
            "processor": "Intel Core i9-13th Gen",
            "gpu": "NVIDIA RTX 4080",
            "ram": "32GB DDR5",
            "storage": "1TB SSD",
            "display": "16-inch QHD 240Hz",
            "refresh_rate": "240Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Alienware m17 R5",
        "brand": "Alienware",
        "category": "Laptops",
        "subcategory": "Gaming Laptops",
        "rent_per_day": 440.0,
        "image_url": "https://m.media-amazon.com/images/I/61IbXh674uL._AC_UY327_FMwebp_QL65_.jpg",
        "description": "Elite gaming machine with RTX 4090 and advanced cooling",
        "specs": {
            "processor": "Intel Core i9-13th Gen",
            "gpu": "NVIDIA RTX 4090",
            "ram": "32GB DDR5",
            "storage": "1TB SSD",
            "display": "17-inch QHD 240Hz",
            "refresh_rate": "240Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "ASUS TUF Gaming F17",
        "brand": "ASUS",
        "category": "Laptops",
        "subcategory": "Gaming Laptops",
        "rent_per_day": 380.0,
        "image_url": "https://m.media-amazon.com/images/I/51CIIx6l+VL._AC_UL480_FMwebp_QL65_.jpg",
        "description": "Durable gaming laptop with RTX 4070 Ti and military-grade durability",
        "specs": {
            "processor": "Intel Core i7-13th Gen",
            "gpu": "NVIDIA RTX 4070 Ti",
            "ram": "16GB DDR5",
            "storage": "512GB SSD",
            "display": "17-inch FHD 144Hz",
            "refresh_rate": "144Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Lenovo Legion Pro 7",
        "brand": "Lenovo",
        "category": "Laptops",
        "subcategory": "Gaming Laptops",
        "rent_per_day": 400.0,
        "image_url": "https://m.media-amazon.com/images/I/71TwTzVcVqL._AC_UL480_FMwebp_QL65_.jpg",
        "description": "Professional gaming laptop with RTX 4080 and superior thermal design",
        "specs": {
            "processor": "Intel Core i9-13th Gen",
            "gpu": "NVIDIA RTX 4080",
            "ram": "32GB DDR5",
            "storage": "1TB SSD",
            "display": "16-inch QHD 165Hz",
            "refresh_rate": "165Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Gigabyte Aorus 17",
        "brand": "Gigabyte",
        "category": "Laptops",
        "subcategory": "Gaming Laptops",
        "rent_per_day": 430.0,
        "image_url": "https://m.media-amazon.com/images/I/51XpiWaeMQL._AC_UL480_FMwebp_QL65_.jpg",
        "description": "High-performance gaming laptop with RTX 4090 and optical switches",
        "specs": {
            "processor": "Intel Core i9-13th Gen",
            "gpu": "NVIDIA RTX 4090",
            "ram": "32GB DDR5",
            "storage": "1TB SSD",
            "display": "17-inch FHD 360Hz",
            "refresh_rate": "360Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Razer Blade Pro 17",
        "brand": "Razer",
        "category": "Laptops",
        "subcategory": "Gaming Laptops",
        "rent_per_day": 490.0,
        "image_url": "https://m.media-amazon.com/images/I/71VG3azYMjL._AC_UY327_FMwebp_QL65_.jpg",
        "description": "Ultra-premium gaming laptop with RTX 4090 and premium design",
        "specs": {
            "processor": "Intel Core i9-13th Gen",
            "gpu": "NVIDIA RTX 4090",
            "ram": "32GB DDR5",
            "storage": "2TB SSD",
            "display": "17-inch QHD 240Hz",
            "refresh_rate": "240Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "MSI GS76 Stealth",
        "brand": "MSI",
        "category": "Laptops",
        "subcategory": "Gaming Laptops",
        "rent_per_day": 410.0,
        "image_url": "https://m.media-amazon.com/images/I/81G1L3nptrL._AC_UY327_FMwebp_QL65_.jpg",
        "description": "Sleek gaming laptop with RTX 4070 Ti and thin bezels",
        "specs": {
            "processor": "Intel Core i7-13th Gen",
            "gpu": "NVIDIA RTX 4070 Ti",
            "ram": "16GB DDR5",
            "storage": "512GB SSD",
            "display": "15-inch QHD 144Hz",
            "refresh_rate": "144Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "HP OMEN 16",
        "brand": "HP",
        "category": "Laptops",
        "subcategory": "Gaming Laptops",
        "rent_per_day": 390.0,
        "image_url": "https://tse1.mm.bing.net/th/id/OIP.Lq9jOBlmTdY-zpFd6q8TFQHaE2",
        "description": "Versatile gaming laptop with RTX 4060 Ti and excellent cooling",
        "specs": {
            "processor": "Intel Core i7-13th Gen",
            "gpu": "NVIDIA RTX 4060 Ti",
            "ram": "16GB DDR5",
            "storage": "512GB SSD",
            "display": "16-inch QHD 165Hz",
            "refresh_rate": "165Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Asus Zephyrus G14",
        "brand": "ASUS",
        "category": "Laptops",
        "subcategory": "Gaming Laptops",
        "rent_per_day": 370.0,
        "image_url": "https://tse1.mm.bing.net/th/id/OIP.aiqE7sUE91cfScmsE3whKAHaEp",
        "description": "Compact gaming powerhouse with RTX 4070 and 240Hz display",
        "specs": {
            "processor": "Intel Core i9-13th Gen",
            "gpu": "NVIDIA RTX 4070",
            "ram": "16GB DDR5",
            "storage": "512GB SSD",
            "display": "14-inch QHD 240Hz",
            "refresh_rate": "240Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Dell G16 Special Edition",
        "brand": "Dell",
        "category": "Laptops",
        "subcategory": "Gaming Laptops",
        "rent_per_day": 360.0,
        "image_url": "https://tse2.mm.bing.net/th/id/OIP.nwiLY5VlVr8PLUFum71l1wHaE8",
        "description": "Feature-rich gaming laptop with RTX 4060 and immersive display",
        "specs": {
            "processor": "Intel Core i7-13th Gen",
            "gpu": "NVIDIA RTX 4060",
            "ram": "16GB DDR5",
            "storage": "512GB SSD",
            "display": "16-inch FHD 144Hz",
            "refresh_rate": "144Hz"
        },
        "availability": True,
        "reviews": []
    }
]

# Check if any gaming laptops already exist
existing_count = products_col.count_documents({"category": "Laptops", "subcategory": "Gaming Laptops"})
if existing_count > 0:
    print(f"Warning: {existing_count} gaming laptop products already exist. Skipping insertion.")
else:
    result = products_col.insert_many(gaming_laptops)
    inserted_ids = result.inserted_ids
    print(f"Inserted: {len(inserted_ids)} gaming laptop products")
    for i, id in enumerate(inserted_ids, 1):
        print(f"  {i}. {id}")
