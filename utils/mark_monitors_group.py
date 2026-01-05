#!/usr/bin/env python
"""
Tag all monitor products with display_group for filtering
"""

from models.db import products_col

# Update all monitors with display_group tag
result = products_col.update_many(
    {"category": "Laptops", "subcategory": "Monitors"},
    {"$set": {"display_group": "laptops_monitors_2025"}}
)

print(f"Matched: {result.matched_count}, Modified: {result.modified_count}")
