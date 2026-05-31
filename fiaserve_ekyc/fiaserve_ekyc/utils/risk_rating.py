from __future__ import annotations

import frappe

REFERENCE_FIELDS = (
	("industry", "KYC Industry", "industry_risk_score"),
	("occupation", "KYC Occupation", "occupation_risk_score"),
	("customer_type", "KYC Customer Type", "customer_type_risk_score"),
	("pep_sanctions_status", "KYC PEP Sanctions Status", "pep_sanctions_risk_score"),
)


def calculate_customer_risk(doc):
	"""Calculate the workbook-style simple-average client risk score."""
	if not doc.get("pep_sanctions_status"):
		doc.set("pep_sanctions_status", "Not Screened")
	scores = []
	for source_field, doctype, target_field in REFERENCE_FIELDS:
		score = _get_reference_score(doctype, doc.get(source_field))
		doc.set(target_field, score or 0)
		if score:
			scores.append(score)

	country = _get_customer_country(doc)
	country_score = _get_country_score(country)
	doc.set("country_risk_score", country_score or 0)
	if country_score:
		scores.append(country_score)

	if len(scores) == 5:
		final_score = round(sum(scores) / 5, 2)
		doc.set("final_risk_score", final_score)
		doc.set("final_risk_rating", get_rating_for_score(final_score))
	else:
		doc.set("final_risk_score", 0)
		doc.set("final_risk_rating", None)


def update_customer_risk(doctype, docname):
	doc = frappe.get_doc(doctype, docname)
	calculate_customer_risk(doc)
	doc.db_update()
	frappe.db.commit()


def get_rating_for_score(score: float) -> str:
	if score <= 2:
		return "Low Risk"
	if score <= 3.5:
		return "Medium Risk"
	return "High Risk"


def _get_reference_score(doctype, name):
	if not name or not frappe.db.exists("DocType", doctype):
		return None
	return frappe.db.get_value(doctype, name, "risk_score")


def _get_country_score(country):
	if not country or not frappe.db.exists("DocType", "Country"):
		return None
	return frappe.db.get_value("Country", country, "kyc_risk_score") or 5


def _get_customer_country(doc):
	for fieldname in ("country_of_residence", "country_of_operations", "country_of_incorporation", "pep_jurisdiction"):
		if doc.get(fieldname):
			return doc.get(fieldname)
	return None
