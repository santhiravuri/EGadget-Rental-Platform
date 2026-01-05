# Mark specific smartphone products with a display_group so catalog can show exactly 9
from models.db import products_col

names = [
    'iPhone 14 Pro',
    'Galaxy S23 Ultra',
    'Pixel 8 Pro',
    'OnePlus 12 Pro',
    'Samsung Galaxy S23',
    'iPhone 14',
    'Pixel 7',
    'Moto G Power',
    'Nokia X20',
]

res = products_col.update_many({'name': {'$in': names}, 'category': 'Mobiles', 'subcategory': 'Smartphones'}, {'$set': {'display_group': 'mobiles_smartphones_2025'}})
print('Matched:', res.matched_count, 'Modified:', res.modified_count)
