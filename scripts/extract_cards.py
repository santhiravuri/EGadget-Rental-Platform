import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
import re

# Extract cards from the Feature Phones catalog instead
c = app.test_client()
r = c.get('/catalog?category=Mobiles&sub=Feature%20Phones')
html = r.get_data(as_text=True)
names = re.findall(r'<h6[^>]*class="card-title[^>]*">([^<]+)</h6>', html)
print('HTTP', r.status_code)
print('Feature Phones cards:', len(names))
for n in names:
    print('-', n)
