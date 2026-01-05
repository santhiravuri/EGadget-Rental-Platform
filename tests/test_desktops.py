#!/usr/bin/env python3
"""
Test script to verify Desktop products are displaying correctly.
"""

import sys
sys.path.insert(0, '.')

from app import app, products_col
import requests
import json

def test_desktops_rendering():
    """Test that Desktops subcategory renders 15 products correctly"""
    client = app.test_client()
    
    # Test: GET /catalog?category=Laptops&sub=Desktops
    print("🔍 Testing: GET /catalog?category=Laptops&sub=Desktops")
    response = client.get('/catalog?category=Laptops&sub=Desktops')
    print(f"  HTTP Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"  ❌ FAILED - Expected 200, got {response.status_code}")
        return False
    
    # Extract product count from rendered HTML
    html = response.data.decode()
    product_count = html.count('col-lg-4')
    print(f"  Products Rendered: {product_count}")
    
    if product_count != 15:
        print(f"  ❌ FAILED - Expected 15 products, got {product_count}")
        return False
    
    print(f"  ✓ PASSED - 15 desktops rendered correctly")
    
    # Verify they're actually in the database
    desktops = list(products_col.find({'display_group': 'laptops_desktops_2025'}))
    print(f"\n📊 Database Verification:")
    print(f"  Desktops in DB: {len(desktops)}")
    
    if len(desktops) != 15:
        print(f"  ❌ FAILED - Expected 15 desktops in DB, got {len(desktops)}")
        return False
    
    # Show product list
    print(f"\n📋 Desktop Products:")
    for i, product in enumerate(desktops, 1):
        price = product.get('rent_per_day', 'N/A')
        print(f"  {i:2}. {product['name']} - ₹{price}/day")
    
    # Check for overlaps with other Laptops subcategories
    gaming_laptops = list(products_col.find({'display_group': 'laptops_gaming_laptops_2025'}))
    monitors = list(products_col.find({'display_group': 'laptops_monitors_2025'}))
    base_laptops = list(products_col.find({'display_group': 'laptops_2025'}))
    
    desktop_ids = set(str(p['_id']) for p in desktops)
    gaming_ids = set(str(p['_id']) for p in gaming_laptops)
    monitor_ids = set(str(p['_id']) for p in monitors)
    base_ids = set(str(p['_id']) for p in base_laptops)
    
    overlaps = {
        'Gaming Laptops': len(desktop_ids & gaming_ids),
        'Monitors': len(desktop_ids & monitor_ids),
        'Base Laptops': len(desktop_ids & base_ids),
    }
    
    print(f"\n🔗 Overlap Check:")
    all_zero = True
    for subcategory, count in overlaps.items():
        status = "✓" if count == 0 else "❌"
        print(f"  {status} Desktops ↔ {subcategory}: {count}")
        if count != 0:
            all_zero = False
    
    if not all_zero:
        print(f"  ❌ FAILED - Found overlapping products!")
        return False
    
    # Verify grid layout (5 full rows on 3-column grid)
    print(f"\n📐 Grid Layout:")
    print(f"  Total Products: {len(desktops)}")
    print(f"  Columns: 3")
    print(f"  Full Rows: {len(desktops) // 3}")
    print(f"  Remainder: {len(desktops) % 3}")
    
    full_rows = len(desktops) // 3
    if full_rows < 3:
        print(f"  ⚠️  WARNING - Grid has only {full_rows} full rows (minimum 3 recommended)")
    else:
        print(f"  ✓ Grid layout adequate ({full_rows} full rows)")
    
    # Test detail page accessibility
    print(f"\n🔗 Testing Product Detail Pages:")
    success_count = 0
    for i, product in enumerate(desktops[:3], 1):  # Test first 3
        product_id = str(product['_id'])
        detail_response = client.get(f'/product/{product_id}')
        status = "✓" if detail_response.status_code == 200 else "❌"
        print(f"  {status} /product/{product_id} - HTTP {detail_response.status_code}")
        if detail_response.status_code == 200:
            success_count += 1
    
    if success_count < 3:
        print(f"  ❌ FAILED - Some detail pages not accessible")
        return False
    
    print(f"\n✅ ALL TESTS PASSED!")
    return True

if __name__ == '__main__':
    success = test_desktops_rendering()
    sys.exit(0 if success else 1)
