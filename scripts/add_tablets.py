#!/usr/bin/env python
"""
Insert 12 tablet products for the Mobiles > Tablets subcategory
"""

from models.db import products_col

tablets = [
    {
        "name": "iPad Pro 11",
        "brand": "Apple",
        "category": "Mobiles",
        "subcategory": "Tablets",
        "rent_per_day": 200.0,
        "image_url": "https://rukminim2.flixcart.com/image/312/312/xif0q/tablet/z/b/c/-original-imahfdyfragxcjsh.jpeg?q=70",
        "description": "Premium 11-inch iPad Pro with M2 chip and 120Hz display",
        "specs": {
            "processor": "Apple M2",
            "ram": "8GB",
            "storage": "128GB",
            "display": "11-inch Liquid Retina XDR",
            "refresh_rate": "120Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Motorola Moto Tab P12",
        "brand": "Motorola",
        "category": "Mobiles",
        "subcategory": "Tablets",
        "rent_per_day": 140.0,
        "image_url": "https://rukminim2.flixcart.com/image/312/312/xif0q/tablet/o/x/w/zag20000in-motorola-original-imahb8mhhnfgf9zy.jpeg?q=70",
        "description": "12-inch Motorola tablet with OLED display and stereo speakers",
        "specs": {
            "processor": "MediaTek Kompanio 1300T",
            "ram": "8GB",
            "storage": "128GB",
            "display": "12-inch OLED",
            "refresh_rate": "90Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Samsung Galaxy Tab S9",
        "brand": "Samsung",
        "category": "Mobiles",
        "subcategory": "Tablets",
        "rent_per_day": 170.0,
        "image_url": "https://rukminim2.flixcart.com/image/312/312/xif0q/tablet/5/d/g/-original-imah9cf9whnm5grh.jpeg?q=70",
        "description": "11-inch Samsung tablet with AMOLED display and S Pen support",
        "specs": {
            "processor": "Snapdragon 8 Gen 1",
            "ram": "8GB",
            "storage": "128GB",
            "display": "11-inch AMOLED",
            "refresh_rate": "120Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "iPad Air 5",
        "brand": "Apple",
        "category": "Mobiles",
        "subcategory": "Tablets",
        "rent_per_day": 180.0,
        "image_url": "https://rukminim2.flixcart.com/image/312/312/xif0q/tablet/z/b/c/-original-imahfdyfragxcjsh.jpeg?q=70",
        "description": "Versatile 10.9-inch iPad Air with M1 chip and stunning display",
        "specs": {
            "processor": "Apple M1",
            "ram": "8GB",
            "storage": "64GB",
            "display": "10.9-inch Liquid Retina",
            "refresh_rate": "60Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Realme Pad 2",
        "brand": "Realme",
        "category": "Mobiles",
        "subcategory": "Tablets",
        "rent_per_day": 100.0,
        "image_url": "https://rukminim2.flixcart.com/image/312/312/xif0q/tablet/5/3/l/rmp2204-realme-original-imagrhcqvxhqqcwf.jpeg?q=70",
        "description": "Budget-friendly 11.5-inch tablet with 144Hz display",
        "specs": {
            "processor": "MediaTek Helio G99",
            "ram": "4GB",
            "storage": "64GB",
            "display": "11.5-inch LCD",
            "refresh_rate": "144Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Realme Pad Pro",
        "brand": "Realme",
        "category": "Mobiles",
        "subcategory": "Tablets",
        "rent_per_day": 110.0,
        "image_url": "https://rukminim2.flixcart.com/image/312/312/xif0q/tablet/o/y/8/rmp2204-realme-original-imagrhcqdhdyc9tg.jpeg?q=70",
        "description": "Premium 12.1-inch Realme tablet with AMOLED display",
        "specs": {
            "processor": "Snapdragon 7 Gen 1",
            "ram": "8GB",
            "storage": "256GB",
            "display": "12.1-inch AMOLED",
            "refresh_rate": "120Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "OnePlus Pad",
        "brand": "OnePlus",
        "category": "Mobiles",
        "subcategory": "Tablets",
        "rent_per_day": 130.0,
        "image_url": "https://rukminim2.flixcart.com/image/312/312/xif0q/tablet/f/k/b/-original-imah4rktdpdfyhbm.jpeg?q=70",
        "description": "11.6-inch OnePlus Pad with 120Hz display and fast charging",
        "specs": {
            "processor": "Snapdragon 8 Gen 1",
            "ram": "8GB",
            "storage": "128GB",
            "display": "11.6-inch LCD",
            "refresh_rate": "120Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Realme Pad 10",
        "brand": "Realme",
        "category": "Mobiles",
        "subcategory": "Tablets",
        "rent_per_day": 90.0,
        "image_url": "https://rukminim2.flixcart.com/image/312/312/ksxjs7k0/tablet/n/j/b/rmp2102-realme-original-imag6e3assqyqhfa.jpeg?q=70",
        "description": "10.3-inch Realme tablet with quad speakers and long battery",
        "specs": {
            "processor": "MediaTek Helio G80",
            "ram": "3GB",
            "storage": "32GB",
            "display": "10.3-inch IPS",
            "refresh_rate": "90Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Realme Pad X",
        "brand": "Realme",
        "category": "Mobiles",
        "subcategory": "Tablets",
        "rent_per_day": 120.0,
        "image_url": "https://rukminim2.flixcart.com/image/312/312/xif0q/tablet/d/c/g/rmp2107-realme-original-imaggf3cfdqtbenn.jpeg?q=70",
        "description": "13-inch Realme Pad X with stylus support and powerful processor",
        "specs": {
            "processor": "MediaTek Kompanio 1300T",
            "ram": "8GB",
            "storage": "256GB",
            "display": "13-inch LCD",
            "refresh_rate": "144Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Realme Pad Mini",
        "brand": "Realme",
        "category": "Mobiles",
        "subcategory": "Tablets",
        "rent_per_day": 80.0,
        "image_url": "https://rukminim2.flixcart.com/image/312/312/ksxjs7k0/tablet/b/3/y/rmp2102-realme-original-imag6e3ay76sxgg4.jpeg?q=70",
        "description": "8.7-inch Realme Pad Mini with compact design and great battery",
        "specs": {
            "processor": "MediaTek Helio G80",
            "ram": "3GB",
            "storage": "32GB",
            "display": "8.7-inch IPS",
            "refresh_rate": "90Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "iPad 10th Gen",
        "brand": "Apple",
        "category": "Mobiles",
        "subcategory": "Tablets",
        "rent_per_day": 150.0,
        "image_url": "https://rukminim2.flixcart.com/image/312/312/xif0q/tablet/e/t/d/-original-imahayydxfug2qkc.jpeg?q=70",
        "description": "10.9-inch iPad with modern design and A14 Bionic chip",
        "specs": {
            "processor": "Apple A14 Bionic",
            "ram": "4GB",
            "storage": "64GB",
            "display": "10.9-inch Liquid Retina",
            "refresh_rate": "60Hz"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Samsung Galaxy Tab A8",
        "brand": "Samsung",
        "category": "Mobiles",
        "subcategory": "Tablets",
        "rent_per_day": 95.0,
        "image_url": "https://rukminim2.flixcart.com/image/312/312/xif0q/tablet/o/o/k/-original-imahayydmeaxc6yg.jpeg?q=70",
        "description": "10.5-inch Samsung tablet with 90Hz display and great speakers",
        "specs": {
            "processor": "MediaTek Helio G80",
            "ram": "4GB",
            "storage": "64GB",
            "display": "10.5-inch IPS",
            "refresh_rate": "90Hz"
        },
        "availability": True,
        "reviews": []
    }
]

# Check if any tablets already exist
existing_count = products_col.count_documents({"category": "Mobiles", "subcategory": "Tablets"})
if existing_count > 0:
    print(f"Warning: {existing_count} tablet products already exist. Skipping insertion.")
else:
    result = products_col.insert_many(tablets)
    inserted_ids = result.inserted_ids
    print(f"Inserted: {len(inserted_ids)} tablet products")
    for i, id in enumerate(inserted_ids, 1):
        print(f"  {i}. {id}")
