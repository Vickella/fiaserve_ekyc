import frappe

COUNTRIES = ["Zimbabwe", "South Africa", "Zambia", "Botswana", "Mozambique", "Namibia", "United Kingdom", "United States"]


def after_install():
    _seed_countries()
    frappe.db.commit()


def _seed_countries():
    if not frappe.db.exists("DocType", "Country"):
        return
    for name in COUNTRIES:
        if not frappe.db.exists("Country", name):
            frappe.get_doc({"doctype": "Country", "country_name": name}).insert(ignore_permissions=True)
