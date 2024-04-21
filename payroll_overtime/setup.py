import frappe 

def after_install():
    add_to_workspace()

def before_uninstall():
    if frappe.db.exists("Workspace", "Shift & Attendance"):
        ws = frappe.get_doc("Workspace", "Shift & Attendance")
        for short in ws.shortcuts:
            if short.label in ["Overtime Request"]:
                ws.remove(short)
                ws.save()
                break

def add_to_workspace():
    if frappe.db.exists("Workspace", "Shift & Attendance"):
        ws = frappe.get_doc("Workspace", "Shift & Attendance")
        ws.append("shortcuts", {
            "type": "DocType",
            "label": "Overtime Request",
            "doc_view": "List",
            "link_to": "Overtime Request"
        })
        ws.save(ignore_permissions=1)