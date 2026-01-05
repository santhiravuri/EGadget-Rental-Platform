#!/usr/bin/env python
"""
Tag all tablet products with display_group for filtering
"""

from models.db import products_col

# Update all tablets with display_group tag
result = products_col.update_many(
    {"category": "Mobiles", "subcategory": "Tablets"},
    {"$set": {"display_group": "mobiles_tablets_2025"}}
)

print(f"Matched: {result.matched_count}, Modified: {result.modified_count}")
