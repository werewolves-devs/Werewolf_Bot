import json

def get_shop_config(shop_file):
    with open(shop_file) as f:
        return json.load(f) # Load shop config file