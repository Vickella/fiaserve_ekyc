import frappe
from frappe.utils import now

from fiaserve_ekyc.fiaserve_ekyc.utils.risk_data import (
	COUNTRY_RISK,
	CUSTOMER_TYPES,
	INDUSTRIES,
	OCCUPATIONS,
	PEP_SANCTIONS_STATUSES,
)

from fiaserve_ekyc.fiaserve_ekyc.utils.seed_data import _seed_country_risk_scores

COUNTRY_RISK_ROWS = [(country, score, rating) for country, (score, rating) in COUNTRY_RISK.items()]

RISK_REFERENCE_DOCTYPES = (
	"kyc_industry",
	"kyc_occupation",
	"kyc_customer_type",
	"kyc_pep_sanctions_status",
	"kyc_country_risk",
)

REFERENCE_SEEDERS = (
	("KYC Industry", "industry", INDUSTRIES),
	("KYC Occupation", "occupation", OCCUPATIONS),
	("KYC Customer Type", "customer_type", CUSTOMER_TYPES),
	("KYC PEP Sanctions Status", "screening_status", PEP_SANCTIONS_STATUSES),
	("KYC Country Risk", "country", COUNTRY_RISK_ROWS),
)


def execute():
	# Ensure the newly added DocType metadata and controller mappings are loaded
	# before inserting reference rows. This keeps the patch safe when a site is
	# migrated from a revision that did not have these DocTypes yet.
	for doctype in RISK_REFERENCE_DOCTYPES:
		frappe.reload_doc("fiaserve_ekyc", "doctype", doctype)

	frappe.clear_cache()
	for doctype, title_field, rows in REFERENCE_SEEDERS:
		_seed_reference_rows_without_controller(doctype, title_field, rows)
	_seed_country_risk_scores()
	frappe.db.commit()


def _seed_reference_rows_without_controller(doctype, title_field, rows):
	"""Seed simple lookup rows without importing the new DocType controllers.

	This patch must run reliably while the same migration is creating the KYC
	reference DocTypes, so it intentionally avoids controller-backed document insertion.
	"""
	if not frappe.db.exists("DocType", doctype) or not _table_exists(doctype):
		return

	table = _table_name(doctype)
	column = _column_name(title_field)
	user = getattr(frappe.session, "user", None) or "Administrator"
	for title, score, rating in rows:
		timestamp = now()
		if _row_exists(table, title):
			frappe.db.sql(
				f"""
				UPDATE {table}
				SET {column}=%s, risk_score=%s, rating=%s, modified=%s, modified_by=%s
				WHERE name=%s
				""",
				(title, score, rating, timestamp, user, title),
			)
			continue

		frappe.db.sql(
			f"""
			INSERT INTO {table}
			(name, creation, modified, modified_by, owner, docstatus, idx, {column}, risk_score, rating)
			VALUES (%s, %s, %s, %s, %s, 0, 0, %s, %s, %s)
			""",
			(title, timestamp, timestamp, user, user, title, score, rating),
		)


def _table_exists(doctype):
	return bool(frappe.db.sql("SHOW TABLES LIKE %s", (f"tab{doctype}",)))


def _row_exists(table, name):
	return bool(frappe.db.sql(f"SELECT name FROM {table} WHERE name=%s LIMIT 1", (name,)))


def _table_name(doctype):
	return "`tab" + doctype.replace("`", "``") + "`"


def _column_name(fieldname):
	return "`" + fieldname.replace("`", "``") + "`"
