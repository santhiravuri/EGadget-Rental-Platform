"""Insert 12 Feature Phone products into the DB (Mobiles -> Feature Phones)
Run: python add_feature_phones.py
"""
from datetime import datetime
from models.db import products_col

phones = [
    {
        "name": "Nokia 105",
        "brand": "Nokia",
        "category": "Mobiles",
        "subcategory": "Feature Phones",
        "rent_per_day": 150.0,
        "image_url": "https://images.pexels.com/photos/28739330/pexels-photo-28739330.jpeg",
        "short_description": "Classic durability with essential calling features.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
    {
        "name": "Itel 5032",
        "brand": "Itel",
        "category": "Mobiles",
        "subcategory": "Feature Phones",
        "rent_per_day": 180.0,
        "image_url": "https://images.pexels.com/photos/20360344/pexels-photo-20360344.jpeg",
        "short_description": "Affordable keypad phone with long battery life.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
    {
        "name": "Vivo T1 Keypad",
        "brand": "Vivo",
        "category": "Mobiles",
        "subcategory": "Feature Phones",
        "rent_per_day": 200.0,
        "image_url": "https://images.pexels.com/photos/16557274/pexels-photo-16557274.jpeg",
        "short_description": "Modern keypad design with smart features.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
    {
        "name": "Kingvoice 105",
        "brand": "Kingvoice",
        "category": "Mobiles",
        "subcategory": "Feature Phones",
        "rent_per_day": 140.0,
        "image_url": "https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/d/e/g/105-single-sim-keypad-mobile-phone-with-wireless-fm-radio-ta-original-imah3kw8zwfwn56h.jpeg?q=70",
        "short_description": "Budget-friendly with wireless FM radio.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
    {
        "name": "Itel 2.4 Inch Display",
        "brand": "Itel",
        "category": "Mobiles",
        "subcategory": "Feature Phones",
        "rent_per_day": 170.0,
        "image_url": "https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/w/m/2/keypad-mobile-2-4-inch-display-type-c-charging-it5032-itel-original-imahgeqdzvyvjkuk.jpeg?q=70",
        "short_description": "Large 2.4 inch display with Type-C charging.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
    {
        "name": "Kingvoice 2.8 Inch",
        "brand": "Kingvoice",
        "category": "Mobiles",
        "subcategory": "Feature Phones",
        "rent_per_day": 160.0,
        "image_url": "https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/t/r/z/it5330-2-8-inch-big-display-1900-mah-battery-kingvoice-it5361-original-imah6k5fspsw2f7u.jpeg?q=70",
        "short_description": "Big 2.8 inch display with 1900 mAh battery.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
    {
        "name": "Kingvoice 130 Music",
        "brand": "Kingvoice",
        "category": "Mobiles",
        "subcategory": "Feature Phones",
        "rent_per_day": 190.0,
        "image_url": "https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/e/s/h/130-music-dual-sim-music-player-wireless-fm-radio-and-dedicated-original-imah3q6f4u5wqkug.jpeg?q=70",
        "short_description": "Music player with dual SIM and FM radio.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
    {
        "name": "Itel 5262",
        "brand": "Itel",
        "category": "Mobiles",
        "subcategory": "Feature Phones",
        "rent_per_day": 175.0,
        "image_url": "https://rukminim2.flixcart.com/image/300/300/xif0q/mobile/j/u/k/it5262-it5262-itel-original-imahfs2qhznzk9ys.jpeg?q=90",
        "short_description": "Compact and portable feature phone.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
    {
        "name": "Vivo T1",
        "brand": "Vivo",
        "category": "Mobiles",
        "subcategory": "Feature Phones",
        "rent_per_day": 210.0,
        "image_url": "https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/w/4/s/t1-v2168-vivo-original-imahaqyp6c3kzmbr.jpeg?q=70",
        "short_description": "Feature phone with modern design.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
    {
        "name": "Vivo Y29 5G",
        "brand": "Vivo",
        "category": "Mobiles",
        "subcategory": "Feature Phones",
        "rent_per_day": 220.0,
        "image_url": "https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/j/g/c/y29-5g-v2420-vivo-original-imahaqg7ugkuq8ce.jpeg?q=70",
        "short_description": "Next-gen feature phone with 5G ready.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
    {
        "name": "Vivo Y300 5G",
        "brand": "Vivo",
        "category": "Mobiles",
        "subcategory": "Feature Phones",
        "rent_per_day": 230.0,
        "image_url": "https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/h/0/f/y300-5g-v2416-vivo-original-imahar5b3yayrwb2.jpeg?q=70",
        "short_description": "Advanced 5G feature phone.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
    {
        "name": "Oppo A18",
        "brand": "Oppo",
        "category": "Mobiles",
        "subcategory": "Feature Phones",
        "rent_per_day": 195.0,
        "image_url": "https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/h/l/s/a18-a18-oppo-original-imah3yhyv6uqmyxz.jpeg?q=70",
        "short_description": "Oppo's reliable feature phone option.",
        "available": True,
        "created_at": datetime.utcnow(),
    },
]

inserted = []
for p in phones:
    q = {"name": p["name"], "category": p["category"], "subcategory": p["subcategory"]}
    existing = products_col.find_one(q)
    if existing:
        print(f"Exists: {p['name']} (skipping)")
    else:
        res = products_col.insert_one(p)
        inserted.append(str(res.inserted_id))
        print(f"Inserted: {p['name']} -> {res.inserted_id}")

print('\nInserted IDs:')
for i in inserted:
    print(' -', i)
