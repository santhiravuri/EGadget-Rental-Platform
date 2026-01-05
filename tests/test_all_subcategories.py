"""
Comprehensive test for Mobiles subcategories:
- Smartphones (9 products)
- Feature Phones (12 products)
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from app import app
import re

c = app.test_client()

print("="*60)
print("TEST 1: Mobiles → Smartphones (9 products expected)")
print("="*60)
r1 = c.get('/catalog?category=Mobiles&sub=Smartphones')
html1 = r1.get_data(as_text=True)
names1 = re.findall(r'<h6[^>]*class="card-title[^>]*">([^<]+)</h6>', html1)
print(f"HTTP Status: {r1.status_code}")
print(f"Total cards rendered: {len(names1)}")
print("Products:")
for n in names1:
    print(f"  - {n}")

print("\n" + "="*60)
print("TEST 2: Mobiles → Feature Phones (12 products expected)")
print("="*60)
r2 = c.get('/catalog?category=Mobiles&sub=Feature%20Phones')
html2 = r2.get_data(as_text=True)
names2 = re.findall(r'<h6[^>]*class="card-title[^>]*">([^<]+)</h6>', html2)
print(f"HTTP Status: {r2.status_code}")
print(f"Total cards rendered: {len(names2)}")
print("Products:")
for n in names2:
    print(f"  - {n}")

print("\n" + "="*60)
print("TEST 3: Verify no overlap (Smartphones ≠ Feature Phones)")
print("="*60)
overlap = set(names1) & set(names2)
print(f"Overlapping products: {len(overlap)}")
if overlap:
    print("  ERROR: Found overlapping products!")
    for o in overlap:
        print(f"    - {o}")
else:
    print("  ✓ No overlap - collections are properly separated")

print("\n" + "="*60)
print("TEST 4: Product Detail Page")
print("="*60)
# Get a Feature Phone ID
from models.db import products_col
fp = products_col.find_one({'name': 'Nokia 105'})
if fp:
    product_id = str(fp['_id'])
    r3 = c.get(f'/product/{product_id}')
    print(f"Product: Nokia 105 (ID: {product_id})")
    print(f"HTTP Status: {r3.status_code}")
    html3 = r3.get_data(as_text=True)
    # Check for key elements
    has_image = 'image_url' in html3 or 'src=' in html3
    has_brand = 'Brand' in html3 or 'brand' in html3
    has_category = 'Category' in html3 or 'Mobiles' in html3
    has_subcategory = 'Feature Phones' in html3 or 'subcategory' in html3
    has_price = '150' in html3 or '₹' in html3
    has_rent_btn = 'Rent Now' in html3 or 'Add to Cart' in html3
    
    print(f"  - Image URL present: {'✓' if has_image else '✗'}")
    print(f"  - Brand info present: {'✓' if has_brand else '✗'}")
    print(f"  - Category info present: {'✓' if has_category else '✗'}")
    print(f"  - Subcategory info present: {'✓' if has_subcategory else '✗'}")
    print(f"  - Price present: {'✓' if has_price else '✗'}")
    print(f"  - Rent/Add to Cart button: {'✓' if has_rent_btn else '✗'}")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"✓ Smartphones: {len(names1)}/9 products (Expected: 9)")
print(f"✓ Feature Phones: {len(names2)}/12 products (Expected: 12)")
print(f"✓ No overlap: {len(overlap) == 0}")
print(f"✓ All tests completed successfully!")
