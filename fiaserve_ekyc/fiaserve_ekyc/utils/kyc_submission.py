import frappe
from frappe import _


ALLOWED_DOCTYPES = {
	"Individual Customer",
	"High Risk PEP Individual",
	"Non-Individual Customer",
	"High Risk Non-Individual",
}


SCREENING_DOCTYPES = {
	"Individual Customer": "Individual Sanctions Screening",
	"High Risk PEP Individual": "High Risk PEP Sanctions Screening",
	"Non-Individual Customer": "Non-Individual Sanctions Screening",
	"High Risk Non-Individual": "High Risk Non-Individual Sanctions Screening",
}


@frappe.whitelist(allow_guest=True)
def submit_kyc(doctype, doc):
	"""Create a KYC record from the public portal and return screening status."""
	if doctype not in ALLOWED_DOCTYPES:
		frappe.throw(_("Unsupported KYC customer type."))

	doc = frappe.parse_json(doc)
	if doc.get("doctype") and doc.get("doctype") != doctype:
		frappe.throw(_("Submitted document type does not match the selected KYC type."))

	clean_doc = _clean_doc(doctype, doc)
	created = frappe.get_doc(clean_doc)
	created.insert(ignore_permissions=True)
	frappe.db.commit()

	screening_doctype = SCREENING_DOCTYPES[doctype]
	return {
		"name": created.name,
		"doctype": doctype,
		"sanctions_status": frappe.db.get_value(doctype, created.name, "sanctions_status"),
		"screening_count": frappe.db.count(screening_doctype, {"customer": created.name}),
	}


@frappe.whitelist(allow_guest=True)
def update_kyc_attachments(doctype, docname, values):
	if doctype not in ALLOWED_DOCTYPES:
		frappe.throw(_("Unsupported KYC customer type."))

	values = frappe.parse_json(values)
	meta = frappe.get_meta(doctype)
	attach_fields = {field.fieldname for field in meta.fields if field.fieldtype == "Attach"}
	updates = {fieldname: value for fieldname, value in values.items() if fieldname in attach_fields}

	if updates:
		frappe.db.set_value(doctype, docname, updates, update_modified=True)
		frappe.db.commit()

	return {"updated": sorted(updates)}


def _clean_doc(doctype, doc):
	meta = frappe.get_meta(doctype)
	allowed_fields = {field.fieldname for field in meta.fields}
	clean_doc = {"doctype": doctype}

	for fieldname, value in doc.items():
		if fieldname == "doctype" or fieldname not in allowed_fields:
			continue
		clean_doc[fieldname] = value

	return clean_doc
