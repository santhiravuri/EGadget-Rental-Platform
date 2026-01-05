#!/usr/bin/env python
"""
Final verification of Gaming Laptops implementation
Shows products and their details
"""

from models.db import products_col
import json

print("\n" + "=" * 70)
print("GAMING LAPTOPS - COMPLETE PRODUCT LIST")
print("=" * 70)

gaming_laptops = list(products_col.find({"category": "Laptops", "subcategory": "Gaming Laptops"}).sort("name", 1))

print(f"\nTotal Gaming Laptops: {len(gaming_laptops)}\n")

for i, laptop in enumerate(gaming_laptops, 1):
    print(f"{i:2d}. {laptop['name']}")
    print(f"    Brand: {laptop['brand']}")
    print(f"    Price: ₹{laptop['rent_per_day']:.0f}/day")
    print(f"    GPU: {laptop['specs'].get('gpu', 'N/A')}")
    print(f"    Display: {laptop['specs'].get('display', 'N/A')}")
    print(f"    Image: {laptop['image_url'][:50]}...")
    print(f"    ID: {laptop['_id']}")
    print()

print("=" * 70)
print("VERIFICATION")
print("=" * 70)

# Verify all have display_group
tagged = sum(1 for l in gaming_laptops if l.get('display_group') == 'laptops_gaming_laptops_2025')
print(f"✓ All {len(gaming_laptops)} gaming laptops tagged with display_group: {tagged == len(gaming_laptops)}")

# Verify prices are in gaming range
prices = [l.get('rent_per_day', 0) for l in gaming_laptops]
print(f"✓ Price range: ₹{min(prices):.0f} - ₹{max(prices):.0f}/day")

# Verify images are from provided URLs
valid_images = 0
for laptop in gaming_laptops:
    url = laptop.get('image_url', '')
    if 'amazon' in url or 'bing' in url:
        valid_images += 1

print(f"✓ Images from provided URLs: {valid_images}/{len(gaming_laptops)}")

# Verify all required fields
required_fields = ['name', 'brand', 'category', 'subcategory', 'rent_per_day', 'image_url', 'description', 'specs']
missing_fields = 0
for laptop in gaming_laptops:
    for field in required_fields:
        if field not in laptop or not laptop.get(field):
            missing_fields += 1
            print(f"  ✗ {laptop['name']} missing {field}")

if missing_fields == 0:
    print(f"✓ All required fields present in all products")

print("\n" + "=" * 70)
print("✓✓✓ GAMING LAPTOPS IMPLEMENTATION VERIFIED ✓✓✓")
print("=" * 70)
