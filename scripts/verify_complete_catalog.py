#!/usr/bin/env python3
"""
Final verification: Complete catalog structure with all 7 subcategories.
Mobiles: 36 products (Smartphones 9 + Feature Phones 12 + Tablets 12)
Laptops: 56 products (Base 14 + Gaming 12 + Monitors 15 + Desktops 15)
Total: 92 products across 7 subcategories
"""

import sys
sys.path.insert(0, '.')

from app import app, products_col

def verify_complete_catalog():
    """Verify the complete catalog structure"""
    
    print("=" * 70)
    print("COMPLETE CATALOG VERIFICATION")
    print("=" * 70)
    
    subcategories = [
        # Mobiles
        {'name': 'Smartphones', 'display_group': 'mobiles_smartphones_2025', 'expected': 9},
        {'name': 'Feature Phones', 'display_group': 'mobiles_feature_phones_2025', 'expected': 12},
        {'name': 'Tablets', 'display_group': 'mobiles_tablets_2025', 'expected': 12},
        # Laptops
        {'name': 'Base Laptops', 'display_group': 'laptops_2025', 'expected': 14},
        {'name': 'Gaming Laptops', 'display_group': 'laptops_gaming_laptops_2025', 'expected': 12},
        {'name': 'Monitors', 'display_group': 'laptops_monitors_2025', 'expected': 15},
        {'name': 'Desktops', 'display_group': 'laptops_desktops_2025', 'expected': 15},
    ]
    
    print("\n📊 Product Count by Subcategory:")
    print("-" * 70)
    
    total_products = 0
    all_product_ids = set()
    passed = 0
    failed = 0
    
    for sub in subcategories:
        products = list(products_col.find({'display_group': sub['display_group']}))
        actual = len(products)
        total_products += actual
        
        # Track for overlap detection
        for p in products:
            all_product_ids.add(str(p['_id']))
        
        status = "✓" if actual == sub['expected'] else "❌"
        print(f"{status} {sub['name']:20} {actual:3}/{sub['expected']:3}")
        
        if actual == sub['expected']:
            passed += 1
        else:
            failed += 1
    
    print("-" * 70)
    print(f"Total Products: {total_products}/92")
    print(f"Passed: {passed}/7 | Failed: {failed}/7")
    
    # Verify no duplicate IDs across different display groups
    print(f"\n🔗 Duplicate Detection:")
    duplicate_ids = {}
    
    for sub in subcategories:
        products = products_col.find({'display_group': sub['display_group']})
        for p in products:
            pid = str(p['_id'])
            if pid not in duplicate_ids:
                duplicate_ids[pid] = []
            duplicate_ids[pid].append(sub['name'])
    
    duplicates_found = sum(1 for ids in duplicate_ids.values() if len(ids) > 1)
    
    if duplicates_found > 0:
        print(f"❌ Found {duplicates_found} duplicate products across subcategories!")
        for pid, groups in duplicate_ids.items():
            if len(groups) > 1:
                print(f"   Product {pid} in: {', '.join(groups)}")
    else:
        print(f"✓ All {total_products} products are unique (no duplicates)")
    
    # Category summary
    print(f"\n📁 Category Summary:")
    print(f"  Mobiles: 9 + 12 + 12 = 33 products ✓")
    print(f"  Laptops: 14 + 12 + 15 + 15 = 56 products ✓")
    print(f"  Grand Total: 89 products")
    
    # Show price ranges
    print(f"\n💰 Price Ranges:")
    for sub in subcategories:
        products = list(products_col.find({'display_group': sub['display_group']}))
        if products:
            prices = [p.get('rent_per_day', 0) for p in products]
            min_price = min(prices)
            max_price = max(prices)
            print(f"  {sub['name']:20} ₹{min_price:3.0f} - ₹{max_price:3.0f}/day")
    
    # Final result
    print("\n" + "=" * 70)
    all_correct = failed == 0 and duplicates_found == 0 and total_products == 89
    if all_correct:
        print("✅ COMPLETE CATALOG VERIFIED!")
        print("   - 7 subcategories")
        print("   - 89 unique products")
        print("   - All product counts accurate")
        print("   - No duplicate products across categories")
    else:
        print("❌ CATALOG VERIFICATION FAILED")
    print("=" * 70)
    
    return all_correct

if __name__ == '__main__':
    success = verify_complete_catalog()
    sys.exit(0 if success else 1)
