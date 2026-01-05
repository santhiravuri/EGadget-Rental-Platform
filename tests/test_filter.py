#!/usr/bin/env python
"""Quick test of subcategory filtering"""
from models.db import products_col
import re

# Test subcategory filter
sub = 'Smartphones'
re_sub = re.compile(rf'^{re.escape(sub)}$', re.IGNORECASE)
filter_q = {'$or': [{'subcategory': re_sub}, {'sub': re_sub}]}
products = list(products_col.find(filter_q))
print(f'Smartphones filter: {len(products)} products found')
for p in products:
    sub_field = p.get('subcategory') or p.get('sub')
    print(f"  - {p.get('name')} (subcategory: {sub_field})")

print("\n" + "="*50 + "\n")

# Test adding id field
for p in products:
    p['id'] = str(p.get('_id'))
    print(f"Product ID (string): {p['id']}")
