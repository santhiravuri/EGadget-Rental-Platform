#!/usr/bin/env python
"""
Delete existing laptop products and prepare for fresh insertion
"""

from models.db import products_col

# Delete existing laptops
result = products_col.delete_many({"category": "Laptops", "subcategory": "Laptops"})
print(f"Deleted: {result.deleted_count} laptop products")
