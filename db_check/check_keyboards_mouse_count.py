from models.db import products_col

cnt = products_col.count_documents({'display_group':'laptops_keyboards_mouse_2025'})
print('Keyboards & Mouse in DB:', cnt)
for p in products_col.find({'display_group':'laptops_keyboards_mouse_2025'}):
    print('-', p.get('name'))
