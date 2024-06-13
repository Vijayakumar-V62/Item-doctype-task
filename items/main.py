import frappe

def get_items():
    items = frappe.get_all('Item', fields=['item_code', 'item_name', 'stock_quantity'])
    for item in items:
        print(f"Item Code: {item.item_code}, Item Name: {item.item_name}, Stock Quantity: {item.stock_quantity}")

get_items()

def get_filtered_sorted_items(item_group):
    items = frappe.get_all('Item', filters={'item_group': item_group}, fields=['item_code', 'item_name', 'stock_quantity'], order_by='item_name asc')
    for item in items:
        print(f"Item Code: {item.item_code}, Item Name: {item.item_name}, Stock Quantity: {item.stock_quantity}")

get_filtered_sorted_items('Item Group Name')

def calculate_total_items():
    total_items = frappe.db.count('Item')
    print(f"Total Items: {total_items}")

calculate_total_items()

def get_items_by_supplier(supplier):
    items = frappe.get_all('Item', filters={'supplier': supplier}, fields=['item_code', 'item_name', 'stock_quantity'])
    for item in items:
        print(f"Item Code: {item.item_code}, Item Name: {item.item_name}, Stock Quantity: {item.stock_quantity}")

get_items_by_supplier('Supplier Name')

def get_items_below_reorder_level():
    items = frappe.get_all('Item', filters={'stock_quantity': ['<', 'reorder_level']}, fields=['item_name', 'stock_quantity'])
    for item in items:
        print(f"Item Name: {item.item_name}, Stock Quantity: {item.stock_quantity}")

get_items_below_reorder_level()
