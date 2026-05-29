import frappe


DEFAULT_LOGO_URL = "/assets/fiaserve_ekyc/images/fiaserv_logo.png"


def apply_portal_context(context):
	context.no_cache = 1
	context.logo_url = frappe.db.get_single_value("Website Settings", "app_logo") or DEFAULT_LOGO_URL
