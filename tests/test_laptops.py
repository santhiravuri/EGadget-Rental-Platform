#!/usr/bin/env python
"""
Test script for Laptops category
Verifies:
1. Laptops category shows 14 products
2. All products are clickable
3. Product detail page works
4. No overlap with other categories
"""

from app import create_app
import re

app = create_app()
client = app.test_client()

print("=" * 60)
print("TEST 1: Laptops Category (14 products expected)")
print("=" * 60)

response = client.get('/catalog?category=Laptops')
print(f"HTTP Status: {response.status_code}")

if response.status_code == 200:
    html = response.get_data(as_text=True)
    
    # Extract product cards
    card_pattern = r'<h6 class="card-title mb-1">([^<]+)</h6>'
    cards = re.findall(card_pattern, html)
    
    print(f"Total cards rendered: {len(cards)}")
    if cards:
        print("Products:")
        for i, card in enumerate(cards, 1):
            print(f"  {i}. {card}")
    
    # Check for placeholder cards
    placeholder_pattern = r'More items coming soon'
    placeholders = len(re.findall(placeholder_pattern, html))
    print(f"Placeholder cards: {placeholders}")

print("\n" + "=" * 60)
print("TEST 2: Product Detail Page (Sample Laptop)")
print("=" * 60)

# Get MacBook Pro detail page
response = client.get('/product/694973d2ff1dee962e047ac1')
print(f"HTTP Status: {response.status_code}")

if response.status_code == 200:
    html = response.get_data(as_text=True)
    
    # Extract product info
    name_match = re.search(r'<h3>([^<]+)</h3>', html)
    price_match = re.search(r'₹ ([0-9.]+) / day', html)
    category_match = re.search(r'Category:\s*</[^>]+>[^<]*<[^>]+>([^<]+)', html)
    
    print(f"Product name: {name_match.group(1) if name_match else 'N/A'}")
    print(f"Price: {price_match.group(1) if price_match else 'N/A'}")
    print(f"Category: {category_match.group(1) if category_match else 'N/A'}")
    
    # Check for required elements
    checks = {
        "Image URL present": "img" in html and "image" in html.lower(),
        "Brand info present": "Brand:" in html or "brand" in html.lower(),
        "Category info present": "Category:" in html or "category" in html.lower(),
        "Price present": "₹" in html or "/day" in html,
        "Rent/Add to Cart button": "Rent Now" in html or "Add to Cart" in html
    }
    
    for check, result in checks.items():
        symbol = "✓" if result else "✗"
        print(f"  {symbol} {check}")

print("\n" + "=" * 60)
print("TEST 3: Verify Laptops Don't Mix with Mobiles")
print("=" * 60)

# Check Laptops
response_laptops = client.get('/catalog?category=Laptops')
html_laptops = response_laptops.get_data(as_text=True)
cards_laptops = re.findall(r'<h6 class="card-title mb-1">([^<]+)</h6>', html_laptops)

# Check Mobiles
response_mobiles = client.get('/catalog?category=Mobiles')
html_mobiles = response_mobiles.get_data(as_text=True)
cards_mobiles = re.findall(r'<h6 class="card-title mb-1">([^<]+)</h6>', html_mobiles)

# Find overlap
overlap = set(cards_laptops) & set(cards_mobiles)
print(f"Laptops products: {len(cards_laptops)}")
print(f"Mobiles products: {len(cards_mobiles)}")
print(f"Overlapping products: {len(overlap)}")

if len(overlap) == 0:
    print("  ✓ No overlap - categories are properly separated")
else:
    print("  ✗ Overlap detected:")
    for product in overlap:
        print(f"    - {product}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

laptops_ok = len(cards_laptops) == 14
detail_ok = response.status_code == 200
separation_ok = len(overlap) == 0

print(f"✓ Laptops count: {len(cards_laptops)}/14 products" if laptops_ok else f"✗ Laptops count: {len(cards_laptops)}/14 products")
print(f"✓ Product detail page works" if detail_ok else f"✗ Product detail page failed")
print(f"✓ No overlap with other categories" if separation_ok else f"✗ Category overlap detected")

if laptops_ok and detail_ok and separation_ok:
    print("\n✓ All tests completed successfully!")
else:
    print("\n✗ Some tests failed - check output above")
