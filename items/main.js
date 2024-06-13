frappe.ui.form.on('Item', {
    refresh: function(frm) {
        set_stock_status(frm);
    },
    stock_quantity: function(frm) {
        set_stock_status(frm);
    }
});

function set_stock_status(frm) {
    if (frm.doc.stock_quantity <= 0) {
        frm.page.wrapper.style.backgroundColor = '#FFCDD2';
    } else if (frm.doc.stock_quantity < frm.doc.reorder_level) {
        frm.page.wrapper.style.backgroundColor = '#FFF9C4';
    } else {
        frm.page.wrapper.style.backgroundColor = '#C8E6C9';
    }
}

frappe.ui.form.on('Item', {
    refresh: function(frm) {
        toggle_supplier_field(frm);
    },
    stock_quantity: function(frm) {
        toggle_supplier_field(frm);
    }
});

function toggle_supplier_field(frm) {
    if (frm.doc.stock_quantity > frm.doc.reorder_level) {
        frm.set_df_property('supplier', 'hidden', 1);
    } else {
        frm.set_df_property('supplier', 'hidden', 0);
    }
}

frappe.ui.form.on('Item', {
    stock_quantity: function(frm) {
        set_stock_status(frm);
    }
});

function set_stock_status(frm) {
    if (frm.doc.stock_quantity <= 0) {
        frm.set_value('stock_status', 'Out of Stock');
    } else if (frm.doc.stock_quantity < frm.doc.reorder_level) {
        frm.set_value('stock_status', 'Low Stock');
    } else {
        frm.set_value('stock_status', 'In Stock');
    }
}

frappe.ui.form.on('Item', {
    before_save: function(frm) {
        if (frm.doc.status_changed) {
            frappe.confirm('Are you sure you want to approve this item?', function() {
                frm.doc.status_changed = false;
                frm.save();
            }, function() {
                frappe.msgprint('Approval canceled');
                frm.doc.status = frm.doc._original_status;
            });
            return false;
        }
        frm.doc._original_status = frm.doc.status;
    },
    status: function(frm) {
        frm.doc.status_changed = true;
    }
});

frappe.ui.form.on('Item', {
    before_save: function(frm) {
        if (frm.doc.reorder_level < 10) {
            frappe.msgprint(__('Reorder level should be at least 10'));
            frappe.validated = false;
        }
    }
});


