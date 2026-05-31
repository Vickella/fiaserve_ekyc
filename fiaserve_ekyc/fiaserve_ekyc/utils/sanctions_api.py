from frappe.utils import now_datetime

SANCTIONS_LISTS = {
    "afdb": "African Development Bank Group Sanctions List",
    "unsc": "United Nations Security Council Consolidated List",
    "eu": "European Union Consolidated Financial Sanctions List",
    "ofac": "Office of Foreign Assets Control Specially Designated Nationals and Blocked Persons List",
    "uk_hmt": "United Kingdom HM Treasury Consolidated List",
    "world_bank": "World Bank Listing of Ineligible Firms and Individuals",
}


def _mark_screening_timestamp(doc, method=None):
    if doc.meta.has_field("sanctions_screened_on"):
        doc.db_set("sanctions_screened_on", now_datetime(), update_modified=False)


def screen_individual(doc, method=None):
    _mark_screening_timestamp(doc, method)


def screen_high_risk_pep(doc, method=None):
    _mark_screening_timestamp(doc, method)


def screen_non_individual(doc, method=None):
    _mark_screening_timestamp(doc, method)


def screen_high_risk_non_individual(doc, method=None):
    _mark_screening_timestamp(doc, method)
