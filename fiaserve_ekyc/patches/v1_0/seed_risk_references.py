import frappe

from fiaserve_ekyc.fiaserve_ekyc.utils.seed_data import _seed_risk_references

RISK_REFERENCE_DOCTYPES = (
	"kyc_industry",
	"kyc_occupation",
	"kyc_customer_type",
	"kyc_pep_sanctions_status",
)


def execute():
	# Ensure the newly added DocType metadata and controller mappings are loaded
	# before inserting reference rows. This keeps the patch safe when a site is
	# migrated from a revision that did not have these DocTypes yet.
	for doctype in RISK_REFERENCE_DOCTYPES:
		frappe.reload_doc("fiaserve_ekyc", "doctype", doctype)

	frappe.clear_cache()
	_seed_risk_references()
	frappe.db.commit()
