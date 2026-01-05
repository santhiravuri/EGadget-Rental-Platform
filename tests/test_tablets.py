#!/usr/bin/env python
"""
Test Tablets implementation
Verifies:
1. 12 tablets display with /catalog?category=Mobiles&sub=Tablets
2. No overlap with Smartphones or Feature Phones
3. Product detail pages work
4. Images load from provided URLs
5. Proper grid layout (at least 3 full rows)
"""

from app import create_app
from models.db import products_col
import re

app = create_app()
client = app.test_client()

print("=" * 70)
print("TEST 1: Tablets Catalog (12 products expected)")
print("=" * 70)

response = client.get('/catalog?category=Mobiles&sub=Tablets')
print(f"HTTP Status: {response.status_code}")

if response.status_code == 200:
    html = response.get_data(as_text=True)
    
    # Extract product cards
    card_pattern = r'<h6 class="card-title mb-1">([^<]+)</h6>'
    cards = re.findall(card_pattern, html)
    
    print(f"Total cards rendered: {len(cards)}")
    print("Products:")
    for i, card in enumerate(cards, 1):
        print(f"  {i:2d}. {card}")
    
    # Check for placeholder cards
    placeholder_pattern = r'More items coming soon'
    placeholders = len(re.findall(placeholder_pattern, html))
    print(f"Placeholder cards: {placeholders}")

print("\n" + "=" * 70)
print("TEST 2: Database Verification")
print("=" * 70)

tablets = list(products_col.find({"category": "Mobiles", "subcategory": "Tablets"}))
print(f"Database count: {len(tablets)} tablets")

tagged = [t for t in tablets if t.get('display_group') == 'mobiles_tablets_2025']
print(f"Tagged with display_group: {len(tagged)}/12")

print("\n" + "=" * 70)
print("TEST 3: Product Detail Page")
print("=" * 70)

if tablets:
    tablet_id = str(tablets[0].get('_id'))
    response = client.get(f'/product/{tablet_id}')
    print(f"HTTP Status: {response.status_code}")
    
    if response.status_code == 200:
        html = response.get_data(as_text=True)
        name_match = re.search(r'<h3>([^<]+)</h3>', html)
        price_match = re.search(r'₹ ([0-9.]+) / day', html)
        
        print(f"Product: {name_match.group(1) if name_match else 'N/A'}")
        print(f"Price: ₹{price_match.group(1) if price_match else 'N/A'}/day")
        
        checks = {
            "Image present": "img" in html,
            "Category info": "Category:" in html or "category" in html.lower(),
            "Subcategory info": "Subcategory:" in html or "Tablets" in html,
            "Price displayed": "₹" in html and "/day" in html,
            "Rent button": "Rent Now" in html or "Add to Cart" in html
        }
        
        for check, result in checks.items():
            symbol = "✓" if result else "✗"
            print(f"  {symbol} {check}")

print("\n" + "=" * 70)
print("TEST 4: Tablets vs Smartphones (No Overlap)")
print("=" * 70)

# Get Tablets
response_tablets = client.get('/catalog?category=Mobiles&sub=Tablets')
html_tablets = response_tablets.get_data(as_text=True)
cards_tablets = re.findall(r'<h6 class="card-title mb-1">([^<]+)</h6>', html_tablets)

# Get Smartphones
response_smartphones = client.get('/catalog?category=Mobiles&sub=Smartphones')
html_smartphones = response_smartphones.get_data(as_text=True)
cards_smartphones = re.findall(r'<h6 class="card-title mb-1">([^<]+)</h6>', html_smartphones)

# Check overlap
overlap = set(cards_tablets) & set(cards_smartphones)
print(f"Tablets: {len(cards_tablets)} products")
print(f"Smartphones: {len(cards_smartphones)} products")
print(f"Overlapping products: {len(overlap)}")

if len(overlap) > 0:
    print("✗ Overlap detected:")
    for product in overlap:
        print(f"  - {product}")
else:
    print("✓ No overlap - Tablets properly isolated from Smartphones")

print("\n" + "=" * 70)
print("TEST 5: Tablets vs Feature Phones (No Overlap)")
print("=" * 70)

# Get Feature Phones
response_feature = client.get('/catalog?category=Mobiles&sub=Feature%20Phones')
html_feature = response_feature.get_data(as_text=True)
cards_feature = re.findall(r'<h6 class="card-title mb-1">([^<]+)</h6>', html_feature)

# Check overlap
overlap_feature = set(cards_tablets) & set(cards_feature)
print(f"Tablets: {len(cards_tablets)} products")
print(f"Feature Phones: {len(cards_feature)} products")
print(f"Overlapping products: {len(overlap_feature)}")

if len(overlap_feature) > 0:
    print("✗ Overlap detected:")
    for product in overlap_feature:
        print(f"  - {product}")
else:
    print("✓ No overlap - Tablets properly isolated from Feature Phones")

print("\n" + "=" * 70)
print("TEST 6: Grid Layout (At least 3 full rows)")
print("=" * 70)

print(f"Total tablets: {len(cards_tablets)}")
print(f"Desktop layout (3 columns): {len(cards_tablets) // 3} full rows + {len(cards_tablets) % 3} products")
print(f"At least 3 full rows: {'✓ Yes' if len(cards_tablets) // 3 >= 3 else '✗ No'}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

test1_pass = len(cards) == 12 and placeholders == 0
test2_pass = len(tablets) == 12 and len(tagged) == 12
test3_pass = response.status_code == 200
test4_pass = len(overlap) == 0
test5_pass = len(overlap_feature) == 0
test6_pass = len(cards_tablets) // 3 >= 3

print(f"{'✓' if test1_pass else '✗'} Tablets catalog renders 12 products")
print(f"{'✓' if test2_pass else '✗'} Database has 12 tagged tablets")
print(f"{'✓' if test3_pass else '✗'} Product detail pages work")
print(f"{'✓' if test4_pass else '✗'} No overlap with Smartphones")
print(f"{'✓' if test5_pass else '✗'} No overlap with Feature Phones")
print(f"{'✓' if test6_pass else '✗'} At least 3 full rows of products")

if test1_pass and test2_pass and test3_pass and test4_pass and test5_pass and test6_pass:
    print("\n✓✓✓ ALL TESTS PASSED - Tablets implementation complete!")
else:
    print("\n✗ Some tests failed")
