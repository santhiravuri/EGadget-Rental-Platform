from models.db import products_col

laptops = list(products_col.find({"category": "Laptops", "subcategory": "Laptops"}))
print(f"Found {len(laptops)} laptop products")
for l in laptops:
    print(f"  - {l['name']} (ID: {l['_id']})")
