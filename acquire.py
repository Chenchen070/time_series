import pandas as pd
import requests

def get_items():
    
    base_url = 'https://python.zgulde.net'
    
    response = requests.get('https://python.zgulde.net/api/v1/items')
    
    data = response.json()
    
    items = data['payload']['items']
    
    while data['payload']['next_page'] is not None:

        response = requests.get(base_url + data['payload']['next_page'])
        data = response.json()
        items += data['payload']['items']
        
    return  pd.DataFrame(items)

def get_store():
    
    response = requests.get('https://python.zgulde.net/api/v1/stores')
    
    data = response.json()

    stores = data['payload']['stores']
    
    return pd.DataFrame(stores)

def get_sales():
    
    response = requests.get('https://python.zgulde.net/api/v1/sales')
    data = response.json()
    sales = data['payload']['sales']
    
    while data['payload']['next_page'] is not None:
        
        response = requests.get('https://python.zgulde.net' + data['payload']['next_page'])
        data = response.json()
        sales += data['payload']['sales']
        
    return pd.DataFrame(sales)

def merge_sales(sales, items, stores):
    
    sales_store_item = sales.merge(stores, how="left", left_on="store", right_on="store_id")
    sales_store_item = sales_store_item.merge(items, how="left", left_on="item", right_on="item_id")
    
    return sales_store_item