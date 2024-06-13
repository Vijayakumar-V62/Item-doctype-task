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


