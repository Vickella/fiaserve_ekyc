import frappe

from fiaserve_ekyc.fiaserve_ekyc.utils.seed_data import _seed_countries


def execute():
	"""Clean stale Desk entries and make country options available on existing sites."""
	for workspace in ("FIASERVE eKYC", "FIASERVE EKYC"):
		if workspace != "FIASERV eKYC" and frappe.db.exists("Workspace", workspace):
			frappe.delete_doc("Workspace", workspace, ignore_permissions=True, force=True)

	_seed_countries()
	frappe.db.commit()
	frappe.clear_cache()
