#!/usr/bin/env python3
"""
Debug script to check what's being rendered for Desktops
"""

import sys
sys.path.insert(0, '.')

from app import app, products_col

def debug_desktops():
    """Debug Desktops rendering"""
    
    # Check database
    print("📊 Database Check:")
    desktops = list(products_col.find({'display_group': 'laptops_desktops_2025'}))
    print(f"  Desktops in DB: {len(desktops)}")
    for product in desktops[:3]:
        print(f"    - {product['name']}")
    
    # Check what the route returns
    client = app.test_client()
    response = client.get('/catalog?category=Laptops&sub=Desktops')
    print(f"\n🌐 HTTP Response:")
    print(f"  Status: {response.status_code}")
    
    html = response.data.decode()
    
    # Count different card types
    print(f"\n📋 Card Count Analysis:")
    print(f"  'product-card' count: {html.count('product-card')}")
    print(f"  'col-lg-4' count: {html.count('col-lg-4')}")
    print(f"  'card' count: {html.count('<div class=\"card\"')}")
    
    # Check for specific product names
    print(f"\n🔍 Product Name Check:")
    product_names = ['Dell OptiPlex', 'Apple iMac', 'HP Pavilion', 'ASUS VivoPC']
    for name in product_names:
        found = 'YES' if name in html else 'NO'
        print(f"  {name}: {found}")
    
    # Show snippet of actual HTML
    print(f"\n📄 HTML Snippet (first 2000 chars of content area):")
    if 'Product Details' in html:
        idx = html.find('Product Details')
        print(html[max(0, idx-500):idx+2000])
    else:
        print(html[1000:3000])

if __name__ == '__main__':
    debug_desktops()
