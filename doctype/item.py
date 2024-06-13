from frappe import _

def validate(doc, method):
    if not doc.item_code or not doc.item_name:
        frappe.throw(_("Item Code and Item Name are mandatory"))
    doc.stock_quantity = sum([bin.actual_qty for bin in frappe.get_all("Bin", filters={"item_code": doc.item_code}, fields=["actual_qty"])])

doctype_js = """
frappe.ui.form.on('Item', {
    refresh: function(frm) {
        set_stock_status(frm);
    },
    stock_quantity: function(frm) {
        set_stock_status(frm);
    },
    onload: function(frm) {
        frm.set_query('item_group', function() {
            return {
                filters: {
                    'is_group': 0
                }
            };
        });
        frm.set_query('supplier', function() {
            return {
                filters: {
                    'is_supplier': 1
                }
            };
        });
    }
});

function set_stock_status(frm) {
    if (frm.doc.stock_quantity <= 0) {
        frm.set_df_property('supplier', 'hidden', 1);
        frm.page.wrapper.style.backgroundColor = '#FFCDD2';
        frm.set_value('stock_status', 'Out of Stock');
    } else if (frm.doc.stock_quantity < frm.doc.reorder_level) {
        frm.set_df_property('supplier', 'hidden', 0);
        frm.page.wrapper.style.backgroundColor = '#FFF9C4';
        frm.set_value('stock_status', 'Low Stock');
    } else {
        frm.set_df_property('supplier', 'hidden', 0);
        frm.page.wrapper.style.backgroundColor = '#C8E6C9';
        frm.set_value('stock_status', 'In Stock');
    }
}
"""

doctype_html = """
{% extends "templates/print_formats/standard.html" %}

{% block content %}
<div class="print-format">
    <div class="header">
        <h2>{{ doc.item_name }}</h2>
        <p>Item Code: {{ doc.item_code }}</p>
        <p>Description: {{ doc.description }}</p>
    </div>
    <div class="table">
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>Item Group</th>
                    <th>Stock Quantity</th>
                    <th>Reorder Level</th>
                    <th>Supplier</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>{{ doc.item_group }}</td>
                    <td>{{ doc.stock_quantity }}</td>
                    <td>{{ doc.reorder_level }}</td>
                    <td>{{ doc.supplier }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
"""

role_permissions_py = """
import frappe

def setup_role_permissions():
    role = frappe.get_doc({
        "doctype": "Role",
        "role_name": "Warehouse Manager",
    })
    role.insert(ignore_permissions=True)

    permissions = [
        {
            "doctype": "Item",
            "role": "Warehouse Manager",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 0
        }
    ]

    for perm in permissions:
        frappe.get_doc(perm).insert(ignore_permissions=True)

setup_role_permissions()
"""

workflow_py = """
import frappe

def setup_workflow():
    workflow = frappe.get_doc({
        "doctype": "Workflow",
        "workflow_name": "Item Workflow",
        "document_type": "Item",
        "is_active": 1,
        "states": [
            {"state": "Under Review", "doc_status": 0, "allow_edit": "Warehouse Manager"},
            {"state": "Approved", "doc_status": 1, "allow_edit": "Warehouse Manager"},
            {"state": "Obsolete", "doc_status": 2, "allow_edit": "Warehouse Manager"},
        ],
        "transitions": [
            {"state": "Under Review", "action": "Approve", "next_state": "Approved", "allow": "Warehouse Manager"},
            {"state": "Approved", "action": "Mark Obsolete", "next_state": "Obsolete", "allow": "Warehouse Manager"},
        ],
        "permissions": [
            {"role": "Warehouse Manager", "state": "Under Review"},
            {"role": "Warehouse Manager", "state": "Approved"},
        ],
    })
    workflow.insert(ignore_permissions=True)

setup_workflow()
"""


