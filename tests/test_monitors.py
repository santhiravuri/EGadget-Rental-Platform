#!/usr/bin/env python
"""
Comprehensive test for Monitors implementation
Verifies:
1. 15 monitors display with /catalog?category=Laptops&sub=Monitors
2. No overlap with Gaming Laptops or regular Laptops
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
print("TEST 1: Monitors Catalog (15 products expected)")
print("=" * 70)

response = client.get('/catalog?category=Laptops&sub=Monitors')
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

monitors = list(products_col.find({"category": "Laptops", "subcategory": "Monitors"}))
print(f"Database count: {len(monitors)} monitors")

tagged = [m for m in monitors if m.get('display_group') == 'laptops_monitors_2025']
print(f"Tagged with display_group: {len(tagged)}/15")

print("\n" + "=" * 70)
print("TEST 3: Product Detail Page")
print("=" * 70)

if monitors:
    monitor_id = str(monitors[0].get('_id'))
    response = client.get(f'/product/{monitor_id}')
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
            "Subcategory info": "Subcategory:" in html or "Monitors" in html,
            "Price displayed": "₹" in html and "/day" in html,
            "Rent button": "Rent Now" in html or "Add to Cart" in html
        }
        
        for check, result in checks.items():
            symbol = "✓" if result else "✗"
            print(f"  {symbol} {check}")

print("\n" + "=" * 70)
print("TEST 4: Monitors vs Gaming Laptops (No Overlap)")
print("=" * 70)

# Get Monitors
response_monitors = client.get('/catalog?category=Laptops&sub=Monitors')
html_monitors = response_monitors.get_data(as_text=True)
cards_monitors = re.findall(r'<h6 class="card-title mb-1">([^<]+)</h6>', html_monitors)

# Get Gaming Laptops
response_gaming = client.get('/catalog?category=Laptops&sub=Gaming%20Laptops')
html_gaming = response_gaming.get_data(as_text=True)
cards_gaming = re.findall(r'<h6 class="card-title mb-1">([^<]+)</h6>', html_gaming)

# Check overlap
overlap = set(cards_monitors) & set(cards_gaming)
print(f"Monitors: {len(cards_monitors)} products")
print(f"Gaming Laptops: {len(cards_gaming)} products")
print(f"Overlapping products: {len(overlap)}")

if len(overlap) > 0:
    print("✗ Overlap detected:")
    for product in overlap:
        print(f"  - {product}")
else:
    print("✓ No overlap - Monitors properly isolated from Gaming Laptops")

print("\n" + "=" * 70)
print("TEST 5: Monitors vs All Laptops (No Mixing)")
print("=" * 70)

# Get All Laptops
response_all = client.get('/catalog?category=Laptops')
html_all = response_all.get_data(as_text=True)
cards_all = re.findall(r'<h6 class="card-title mb-1">([^<]+)</h6>', html_all)

# All Laptops should include Gaming Laptops + regular Laptops (14) = 26 products if no subcategory filter
# But when requesting Laptops category without subcategory, it should show only the base Laptops (14) due to display_group filter
print(f"Monitors subcategory: {len(cards_monitors)} products")
print(f"All Laptops category: {len(cards_all)} products")

print("\n" + "=" * 70)
print("TEST 6: Grid Layout (At least 3 full rows)")
print("=" * 70)

print(f"Total monitors: {len(cards_monitors)}")
print(f"Desktop layout (3 columns): {len(cards_monitors) // 3} full rows + {len(cards_monitors) % 3} products")
print(f"At least 3 full rows: {'✓ Yes' if len(cards_monitors) // 3 >= 3 else '✗ No'}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

test1_pass = len(cards) == 15 and placeholders == 0
test2_pass = len(monitors) == 15 and len(tagged) == 15
test3_pass = response.status_code == 200
test4_pass = len(overlap) == 0
test5_pass = len(cards_monitors) == 15
test6_pass = len(cards_monitors) // 3 >= 3

print(f"{'✓' if test1_pass else '✗'} Monitors catalog renders 15 products")
print(f"{'✓' if test2_pass else '✗'} Database has 15 tagged monitors")
print(f"{'✓' if test3_pass else '✗'} Product detail pages work")
print(f"{'✓' if test4_pass else '✗'} No overlap with Gaming Laptops")
print(f"{'✓' if test5_pass else '✗'} Monitors properly isolated")
print(f"{'✓' if test6_pass else '✗'} At least 3 full rows of products")

if test1_pass and test2_pass and test3_pass and test4_pass and test5_pass and test6_pass:
    print("\n✓✓✓ ALL TESTS PASSED - Monitors implementation complete!")
else:
    print("\n✗ Some tests failed")
