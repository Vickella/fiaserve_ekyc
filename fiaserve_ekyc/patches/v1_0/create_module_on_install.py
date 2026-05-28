import frappe


def execute():
	if not frappe.db.exists("Module Def", "FIASERVE EKYC"):
		frappe.get_doc({"doctype": "Module Def", "module_name": "FIASERVE EKYC", "app_name": "fiaserve_ekyc"}).insert(ignore_permissions=True)
	frappe.db.commit()
