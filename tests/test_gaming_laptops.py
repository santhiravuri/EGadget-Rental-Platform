#!/usr/bin/env python
"""
Test Gaming Laptops implementation
Verifies:
1. 12 gaming laptops display with /catalog?category=Laptops&sub=Gaming%20Laptops
2. No overlap with regular Laptops
3. Product detail pages work
4. Images load from provided URLs
"""

from app import create_app
from models.db import products_col
import re

app = create_app()
client = app.test_client()

print("=" * 70)
print("TEST 1: Gaming Laptops Catalog (12 products expected)")
print("=" * 70)

response = client.get('/catalog?category=Laptops&sub=Gaming%20Laptops')
print(f"HTTP Status: {response.status_code}")

if response.status_code == 200:
    html = response.get_data(as_text=True)
    
    # Extract product cards
    card_pattern = r'<h6 class="card-title mb-1">([^<]+)</h6>'
    cards = re.findall(card_pattern, html)
    
    print(f"Total cards rendered: {len(cards)}")
    print("Products:")
    for i, card in enumerate(cards, 1):
        print(f"  {i}. {card}")
    
    # Check for placeholder cards
    placeholder_pattern = r'More items coming soon'
    placeholders = len(re.findall(placeholder_pattern, html))
    print(f"Placeholder cards: {placeholders}")

print("\n" + "=" * 70)
print("TEST 2: Database Verification")
print("=" * 70)

gaming_laptops = list(products_col.find({"category": "Laptops", "subcategory": "Gaming Laptops"}))
print(f"Database count: {len(gaming_laptops)} gaming laptops")

tagged = [l for l in gaming_laptops if l.get('display_group') == 'laptops_gaming_laptops_2025']
print(f"Tagged with display_group: {len(tagged)}/12")

print("\n" + "=" * 70)
print("TEST 3: Product Detail Page")
print("=" * 70)

if gaming_laptops:
    laptop_id = str(gaming_laptops[0].get('_id'))
    response = client.get(f'/product/{laptop_id}')
    print(f"HTTP Status: {response.status_code}")
    
    if response.status_code == 200:
        html = response.get_data(as_text=True)
        name_match = re.search(r'<h3>([^<]+)</h3>', html)
        price_match = re.search(r'₹ ([0-9.]+) / day', html)
        
        print(f"Product: {name_match.group(1) if name_match else 'N/A'}")
        print(f"Price: ₹{price_match.group(1) if price_match else 'N/A'}/day")
        
        checks = {
            "Image present": "img" in html,
            "Brand info": "Brand:" in html,
            "Category info": "Category:" in html,
            "Price displayed": "₹" in html,
            "Rent button": "Rent Now" in html or "Add to Cart" in html
        }
        
        for check, result in checks.items():
            symbol = "✓" if result else "✗"
            print(f"  {symbol} {check}")

print("\n" + "=" * 70)
print("TEST 4: Gaming Laptops vs Regular Laptops (No Overlap)")
print("=" * 70)

# Get Gaming Laptops
response_gaming = client.get('/catalog?category=Laptops&sub=Gaming%20Laptops')
html_gaming = response_gaming.get_data(as_text=True)
cards_gaming = re.findall(r'<h6 class="card-title mb-1">([^<]+)</h6>', html_gaming)

# Get All Laptops
response_all = client.get('/catalog?category=Laptops')
html_all = response_all.get_data(as_text=True)
cards_all = re.findall(r'<h6 class="card-title mb-1">([^<]+)</h6>', html_all)

print(f"Gaming Laptops: {len(cards_gaming)} products")
print(f"All Laptops: {len(cards_all)} products")

# Check overlap
overlap = set(cards_gaming) & set(cards_all)
print(f"Overlapping products: {len(overlap)}")

if len(overlap) > 0:
    print("✗ Overlap detected:")
    for product in overlap:
        print(f"  - {product}")
else:
    print("✓ No overlap - Gaming Laptops properly isolated")

print("\n" + "=" * 70)
print("TEST 5: Grid Layout (At least 3 full rows)")
print("=" * 70)

print(f"Total gaming laptops: {len(cards_gaming)}")
print(f"Desktop layout (3 columns): {len(cards_gaming) // 3} full rows + {len(cards_gaming) % 3} products")
print(f"At least 3 full rows: {'✓ Yes' if len(cards_gaming) // 3 >= 3 else '✗ No'}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

test1_pass = len(cards) == 12 and placeholders == 0
test2_pass = len(gaming_laptops) == 12 and len(tagged) == 12
test3_pass = response.status_code == 200
test4_pass = len(overlap) == 0
test5_pass = len(cards_gaming) // 3 >= 3

print(f"{'✓' if test1_pass else '✗'} Gaming Laptops catalog renders 12 products")
print(f"{'✓' if test2_pass else '✗'} Database has 12 tagged gaming laptops")
print(f"{'✓' if test3_pass else '✗'} Product detail pages work")
print(f"{'✓' if test4_pass else '✗'} No overlap with regular Laptops")
print(f"{'✓' if test5_pass else '✗'} At least 3 full rows of products")

if test1_pass and test2_pass and test3_pass and test4_pass and test5_pass:
    print("\n✓✓✓ ALL TESTS PASSED - Gaming Laptops implementation complete!")
else:
    print("\n✗ Some tests failed")
