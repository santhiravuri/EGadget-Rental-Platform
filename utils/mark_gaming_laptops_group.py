#!/usr/bin/env python
"""
Tag all gaming laptop products with display_group for filtering
"""

from models.db import products_col

# Update all gaming laptops with display_group tag
result = products_col.update_many(
    {"category": "Laptops", "subcategory": "Gaming Laptops"},
    {"$set": {"display_group": "laptops_gaming_laptops_2025"}}
)

print(f"Matched: {result.matched_count}, Modified: {result.modified_count}")
