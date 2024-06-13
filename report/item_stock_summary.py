import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Item Code"), "fieldname": "item_code", "fieldtype": "Data", "width": 100},
        {"label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data", "width": 150},
        {"label": _("Stock Quantity"), "fieldname": "stock_quantity", "fieldtype": "Float", "width": 100},
        {"label": _("Reorder Level"), "fieldname": "reorder_level", "fieldtype": "Float", "width": 100},
        {"label": _("Supplier"), "fieldname": "supplier", "fieldtype": "Link", "options": "Supplier", "width": 150},
    ]

def get_data(filters):
    conditions = ""
    if filters.get("supplier"):
        conditions += " AND supplier = %(supplier)s"
    
    items = frappe.db.sql("""
        SELECT 
            item_code, item_name, stock_quantity, reorder_level, supplier
        FROM
            `tabItem`
        WHERE
            1 = 1 {conditions}
        """.format(conditions=conditions), filters, as_dict=1)

    return items

def get_summary():
    total_items = frappe.db.count('Item')
    low_stock_items = frappe.db.count('Item', filters={'stock_quantity': ['<', 'reorder_level']})
    supplier_wise_stock = frappe.db.sql("""
        SELECT 
            supplier, COUNT(*) as item_count
        FROM
            `tabItem`
        GROUP BY
            supplier
    """, as_dict=1)

    return {
        'total_items': total_items,
        'low_stock_items': low_stock_items,
        'supplier_wise_stock': supplier_wise_stock
    }


