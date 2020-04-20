import json
import enum
import sys


data = {'location': int(sys.argv[1])}

with open('order/order_A/config.json', 'w') as f:
    json.dump(data, f)
with open('order/order_B/config.json', 'w') as f:
    json.dump(data, f)
with open('catalogue/catalog_A/config.json', 'w') as f:
    json.dump(data, f)
with open('catalogue/catalog_B/config.json', 'w') as f:
    json.dump(data, f)
with open('front-end/config.json', 'w') as f:
    json.dump(data, f)
with open('config.json', 'w') as f:
    json.dump(data, f)
