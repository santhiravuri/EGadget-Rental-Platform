from models.db import products_col

cnt = products_col.count_documents({'display_group':'mobiles_mobile_accessories_2025'})
print('Mobile Accessories in DB:', cnt)
for p in products_col.find({'display_group':'mobiles_mobile_accessories_2025'}):
    print('-', p.get('name'))
