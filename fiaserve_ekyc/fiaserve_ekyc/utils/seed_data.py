import frappe
from frappe.utils import now

from fiaserve_ekyc.fiaserve_ekyc.utils.risk_data import (
	COUNTRY_RISK,
	CUSTOMER_TYPES,
	INDUSTRIES,
	OCCUPATIONS,
	PEP_SANCTIONS_STATUSES,
)

COUNTRIES = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo (Brazzaville)', 'Congo (Kinshasa)', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Korea (North)', 'Korea (South)', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']

COUNTRY_ALIASES = {
	"usa": "United States",
	"u.s.a.": "United States",
	"u.s.": "United States",
	"us": "United States",
	"united states of america": "United States",
	"uk": "United Kingdom",
	"u.k.": "United Kingdom",
	"brunei darussalam": "Brunei",
	"russian federation": "Russia",
	"syrian arab republic": "Syria",
	"viet nam": "Vietnam",
	"swaziland": "Eswatini",
	"congo": "Congo (Brazzaville)",
	"congo (democratic republic)": "Congo (Kinshasa)",
}


def after_install():
	_seed_countries()
	_seed_risk_references()
	frappe.db.commit()


def after_migrate():
	"""Keep KYC risk references available after every migrate/model sync."""
	_seed_risk_references()
	frappe.db.commit()


def _seed_countries():
	if not frappe.db.exists("DocType", "Country"):
		return
	for name in COUNTRIES:
		ensure_country(name)


def normalize_country_name(name):
	if not name:
		return ""
	clean_name = " ".join(str(name).split())
	return COUNTRY_ALIASES.get(clean_name.lower(), clean_name)


def ensure_country(name):
	"""Return a valid Country link value, creating the Country if it is missing."""
	name = normalize_country_name(name)
	if not name or not frappe.db.exists("DocType", "Country"):
		return name
	if frappe.db.exists("Country", name):
		return name

	existing = frappe.db.get_value("Country", {"country_name": name}, "name")
	if existing:
		return existing

	doc = frappe.get_doc({"doctype": "Country", "country_name": name})
	doc.insert(ignore_permissions=True)
	return doc.name



def _seed_risk_references():
	_seed_reference_rows("KYC Industry", "industry", INDUSTRIES)
	_seed_reference_rows("KYC Occupation", "occupation", OCCUPATIONS)
	_seed_reference_rows("KYC Customer Type", "customer_type", CUSTOMER_TYPES)
	_seed_reference_rows("KYC PEP Sanctions Status", "screening_status", PEP_SANCTIONS_STATUSES)
	_seed_country_risk_scores()


def _seed_reference_rows(doctype, title_field, rows):
	if not frappe.db.exists("DocType", doctype) or not _table_exists(doctype):
		return

	table = _table_name(doctype)
	user = getattr(frappe.session, "user", None) or "Administrator"
	for title, score, rating in rows:
		timestamp = now()
		if _row_exists(table, title):
			frappe.db.sql(
				f"""
				UPDATE {table}
				SET {title_field}=%s, risk_score=%s, rating=%s, modified=%s, modified_by=%s
				WHERE name=%s
				""",
				(title, score, rating, timestamp, user, title),
			)
			continue

		frappe.db.sql(
			f"""
			INSERT INTO {table}
			(name, creation, modified, modified_by, owner, docstatus, idx, {title_field}, risk_score, rating)
			VALUES (%s, %s, %s, %s, %s, 0, 0, %s, %s, %s)
			""",
			(title, timestamp, timestamp, user, user, title, score, rating),
		)


def _table_exists(doctype):
	return bool(frappe.db.sql("SHOW TABLES LIKE %s", f"tab{doctype}"))


def _row_exists(table, name):
	return bool(frappe.db.sql(f"SELECT name FROM {table} WHERE name=%s LIMIT 1", (name,)))


def _table_name(doctype):
	return "`tab" + doctype.replace("`", "``") + "`"


def _seed_country_risk_scores():
	if not frappe.db.exists("DocType", "Country"):
		return
	ensure_country_risk_fields()
	for country, (score, rating) in COUNTRY_RISK.items():
		name = ensure_country(country)
		if frappe.db.exists("Country", name):
			frappe.db.set_value("Country", name, {"kyc_risk_score": score, "kyc_risk_rating": rating})


def ensure_country_risk_fields():
	if not frappe.db.exists("DocType", "Country"):
		return
	for fieldname, label, fieldtype, options in (
		("kyc_risk_score", "KYC Risk Score", "Int", None),
		("kyc_risk_rating", "KYC Risk Rating", "Select", "Low\nMedium\nHigh\nAuto High"),
	):
		if frappe.db.exists("Custom Field", {"dt": "Country", "fieldname": fieldname}):
			continue
		frappe.get_doc({
			"doctype": "Custom Field",
			"dt": "Country",
			"fieldname": fieldname,
			"label": label,
			"fieldtype": fieldtype,
			"options": options,
		}).insert(ignore_permissions=True)
