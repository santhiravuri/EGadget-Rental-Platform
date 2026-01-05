# Mark specific Feature Phone products with a display_group
from models.db import products_col

names = [
    'Nokia 105',
    'Itel 5032',
    'Vivo T1 Keypad',
    'Kingvoice 105',
    'Itel 2.4 Inch Display',
    'Kingvoice 2.8 Inch',
    'Kingvoice 130 Music',
    'Itel 5262',
    'Vivo T1',
    'Vivo Y29 5G',
    'Vivo Y300 5G',
    'Oppo A18',
]

res = products_col.update_many({'name': {'$in': names}, 'category': 'Mobiles', 'subcategory': 'Feature Phones'}, {'$set': {'display_group': 'mobiles_feature_phones_2025'}})
print('Matched:', res.matched_count, 'Modified:', res.modified_count)
