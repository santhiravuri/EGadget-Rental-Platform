#!/usr/bin/env python
"""
Tag all desktop products with display_group for filtering
"""

from models.db import products_col

# Update all desktops with display_group tag
result = products_col.update_many(
    {"category": "Laptops", "subcategory": "Desktops"},
    {"$set": {"display_group": "laptops_desktops_2025"}}
)

print(f"Matched: {result.matched_count}, Modified: {result.modified_count}")
