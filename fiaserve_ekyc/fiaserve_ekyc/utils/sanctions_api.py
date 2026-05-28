import frappe
from frappe.utils import now_datetime


def _mark_screening(doc, method=None):
    doc.db_set("sanctions_status", "Pending", update_modified=False)
    if doc.meta.has_field("sanctions_screened_on"):
        doc.db_set("sanctions_screened_on", now_datetime(), update_modified=False)


def screen_individual(doc, method=None):
    _mark_screening(doc, method)


def screen_high_risk_pep(doc, method=None):
    _mark_screening(doc, method)


def screen_non_individual(doc, method=None):
    _mark_screening(doc, method)


def screen_high_risk_non_individual(doc, method=None):
    _mark_screening(doc, method)
