#!/usr/bin/env python
"""
Insert 15 monitor products for the Laptops > Monitors subcategory
"""

from models.db import products_col

monitors = [
    {
        "name": "Dell S2722DGM 27-inch",
        "brand": "Dell",
        "category": "Laptops",
        "subcategory": "Monitors",
        "rent_per_day": 120.0,
        "image_url": "https://m.media-amazon.com/images/I/81r4H4+w+FL._AC_UY327_FMwebp_QL65_.jpg",
        "description": "27-inch gaming monitor with 240Hz refresh rate and QHD resolution",
        "specs": {
            "size": "27 inches",
            "resolution": "2560 x 1440 (QHD)",
            "panel_type": "IPS",
            "refresh_rate": "240Hz",
            "response_time": "1ms"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "LG UltraGear 32-inch",
        "brand": "LG",
        "category": "Laptops",
        "subcategory": "Monitors",
        "rent_per_day": 140.0,
        "image_url": "https://m.media-amazon.com/images/I/71SPo9rj0WL._AC_UY327_FMwebp_QL65_.jpg",
        "description": "32-inch curved gaming monitor with 4K resolution and 144Hz refresh",
        "specs": {
            "size": "32 inches",
            "resolution": "3840 x 2160 (4K)",
            "panel_type": "VA",
            "refresh_rate": "144Hz",
            "response_time": "1ms"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "ASUS ProArt PA278QV",
        "brand": "ASUS",
        "category": "Laptops",
        "subcategory": "Monitors",
        "rent_per_day": 130.0,
        "image_url": "https://m.media-amazon.com/images/I/815UZPn8WUL._AC_UY327_FMwebp_QL65_.jpg",
        "description": "27-inch professional monitor with 100% sRGB color accuracy",
        "specs": {
            "size": "27 inches",
            "resolution": "2560 x 1440 (QHD)",
            "panel_type": "IPS",
            "refresh_rate": "60Hz",
            "color_accuracy": "100% sRGB"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "BenQ PD2700U 4K Designer",
        "brand": "BenQ",
        "category": "Laptops",
        "subcategory": "Monitors",
        "rent_per_day": 150.0,
        "image_url": "https://m.media-amazon.com/images/I/71I0KQmcYBL._AC_UY327_FMwebp_QL65_.jpg",
        "description": "27-inch 4K professional monitor with hardware calibration",
        "specs": {
            "size": "27 inches",
            "resolution": "3840 x 2160 (4K)",
            "panel_type": "IPS",
            "refresh_rate": "60Hz",
            "color_accuracy": "100% sRGB"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Samsung LU28E590DS 4K Monitor",
        "brand": "Samsung",
        "category": "Laptops",
        "subcategory": "Monitors",
        "rent_per_day": 110.0,
        "image_url": "https://images.unsplash.com/photo-1616763355548-1b606f439f86?w=600&auto=format&fit=crop&q=60",
        "description": "28-inch 4K UHD monitor with LED backlit display",
        "specs": {
            "size": "28 inches",
            "resolution": "3840 x 2160 (4K)",
            "panel_type": "TN",
            "refresh_rate": "60Hz",
            "response_time": "1ms"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "LG 29UP550 UltraWide",
        "brand": "LG",
        "category": "Laptops",
        "subcategory": "Monitors",
        "rent_per_day": 115.0,
        "image_url": "https://images.unsplash.com/photo-1615130241719-44ad5e69e14e?w=600&auto=format&fit=crop&q=60",
        "description": "29-inch UltraWide monitor with HDR support and USB-C connectivity",
        "specs": {
            "size": "29 inches",
            "resolution": "2560 x 1080 (UltraWide)",
            "panel_type": "IPS",
            "refresh_rate": "60Hz",
            "hdr_support": "Yes"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Acer Predator X34 Gaming",
        "brand": "Acer",
        "category": "Laptops",
        "subcategory": "Monitors",
        "rent_per_day": 160.0,
        "image_url": "https://plus.unsplash.com/premium_photo-1678564741870-d68a69925537?w=600&auto=format&fit=crop&q=60",
        "description": "34-inch ultrawide curved gaming monitor with 165Hz refresh rate",
        "specs": {
            "size": "34 inches",
            "resolution": "3440 x 1440 (UltraWide)",
            "panel_type": "IPS",
            "refresh_rate": "165Hz",
            "curve_radius": "1900R"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Corsair Xeneon 32 UltraWide",
        "brand": "Corsair",
        "category": "Laptops",
        "subcategory": "Monitors",
        "rent_per_day": 170.0,
        "image_url": "https://images.unsplash.com/photo-1632582204758-5ac65783517a?w=600&auto=format&fit=crop&q=60",
        "description": "32-inch ultrawide gaming monitor with 240Hz and quantum dots",
        "specs": {
            "size": "32 inches",
            "resolution": "3840 x 1080 (UltraWide)",
            "panel_type": "VA",
            "refresh_rate": "240Hz",
            "color_gamut": "Quantum Dots"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "HP Z27 Professional 4K",
        "brand": "HP",
        "category": "Laptops",
        "subcategory": "Monitors",
        "rent_per_day": 135.0,
        "image_url": "https://m.media-amazon.com/images/I/81K8IpnFcZL._AC_UY327_FMwebp_QL65_.jpg",
        "description": "27-inch 4K professional monitor with DreamColor technology",
        "specs": {
            "size": "27 inches",
            "resolution": "3840 x 2160 (4K)",
            "panel_type": "IPS",
            "refresh_rate": "60Hz",
            "color_accuracy": "99.6% Adobe RGB"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "ViewSonic VP2468a 24-inch Professional",
        "brand": "ViewSonic",
        "category": "Laptops",
        "subcategory": "Monitors",
        "rent_per_day": 100.0,
        "image_url": "https://m.media-amazon.com/images/I/81-pe8AZQLL._AC_UY327_FMwebp_QL65_.jpg",
        "description": "24-inch professional monitor with color calibration support",
        "specs": {
            "size": "24 inches",
            "resolution": "1920 x 1200 (WUXGA)",
            "panel_type": "IPS",
            "refresh_rate": "60Hz",
            "color_accuracy": "100% sRGB"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "ASUS VG279Q Gaming 27-inch",
        "brand": "ASUS",
        "category": "Laptops",
        "subcategory": "Monitors",
        "rent_per_day": 125.0,
        "image_url": "https://tse1.mm.bing.net/th/id/OIP.siGv78Ce6asx3bOnOWvYbQHaFi?pid=Api&P=0&h=180",
        "description": "27-inch gaming monitor with 165Hz refresh and adaptive sync",
        "specs": {
            "size": "27 inches",
            "resolution": "1920 x 1080 (FHD)",
            "panel_type": "IPS",
            "refresh_rate": "165Hz",
            "adaptive_sync": "FreeSync & GSync"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "MSI Optix MAG321CURV",
        "brand": "MSI",
        "category": "Laptops",
        "subcategory": "Monitors",
        "rent_per_day": 145.0,
        "image_url": "https://tse2.mm.bing.net/th/id/OIP.SasmM-GQXglU0qXvA_CXtwHaE0?pid=Api&P=0&h=180",
        "description": "32-inch curved gaming monitor with 165Hz and VA panel",
        "specs": {
            "size": "32 inches",
            "resolution": "2560 x 1440 (QHD)",
            "panel_type": "VA",
            "refresh_rate": "165Hz",
            "curve_radius": "1500R"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Gigabyte M32U 32-inch 4K Gaming",
        "brand": "Gigabyte",
        "category": "Laptops",
        "subcategory": "Monitors",
        "rent_per_day": 155.0,
        "image_url": "https://tse3.mm.bing.net/th/id/OIP.KVESJD3n-IAVwedYOeWluQHaEK?pid=Api&P=0&h=180",
        "description": "32-inch 4K gaming monitor with 144Hz IPS panel",
        "specs": {
            "size": "32 inches",
            "resolution": "3840 x 2160 (4K)",
            "panel_type": "IPS",
            "refresh_rate": "144Hz",
            "hdr_support": "DisplayHDR 600"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Dell S3220DGF 32-inch Curved",
        "brand": "Dell",
        "category": "Laptops",
        "subcategory": "Monitors",
        "rent_per_day": 130.0,
        "image_url": "https://tse3.mm.bing.net/th/id/OIP.GmGrl9UU7cssMEwZq1znmwHaEO?pid=Api&P=0&h=180",
        "description": "32-inch curved monitor with QHD resolution and 144Hz refresh",
        "specs": {
            "size": "32 inches",
            "resolution": "2560 x 1440 (QHD)",
            "panel_type": "VA",
            "refresh_rate": "144Hz",
            "curve_radius": "1800R"
        },
        "availability": True,
        "reviews": []
    },
    {
        "name": "Eizo ColorEdge CG279X",
        "brand": "Eizo",
        "category": "Laptops",
        "subcategory": "Monitors",
        "rent_per_day": 165.0,
        "image_url": "https://tse4.mm.bing.net/th/id/OIP.mGCM6NWay7Emj-26nJ8TmgHaE8?pid=Api&P=0&h=180",
        "description": "27-inch color-critical monitor with hardware calibration",
        "specs": {
            "size": "27 inches",
            "resolution": "2560 x 1440 (QHD)",
            "panel_type": "IPS",
            "refresh_rate": "60Hz",
            "color_accuracy": "99.3% Adobe RGB"
        },
        "availability": True,
        "reviews": []
    }
]

# Check if any monitors already exist
existing_count = products_col.count_documents({"category": "Laptops", "subcategory": "Monitors"})
if existing_count > 0:
    print(f"Warning: {existing_count} monitor products already exist. Skipping insertion.")
else:
    result = products_col.insert_many(monitors)
    inserted_ids = result.inserted_ids
    print(f"Inserted: {len(inserted_ids)} monitor products")
    for i, id in enumerate(inserted_ids, 1):
        print(f"  {i}. {id}")
