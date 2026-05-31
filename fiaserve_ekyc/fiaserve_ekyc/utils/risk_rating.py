import frappe

RISK_RATING_COMPONENTS = (
    ("industry", "KYC Industry", "industry_risk_score"),
    ("occupation", "KYC Occupation", "occupation_risk_score"),
    ("customer_type", "KYC Customer Type", "customer_type_risk_score"),
    ("owner_screening_status", "KYC PEP Sanctions Status", "pep_sanctions_risk_score"),
)

COUNTRY_FIELDS = ("country_of_residence", "country_of_business_operations")


def apply_risk_rating(doc):
    scores = []
    notes = []

    for source_field, doctype, target_field in RISK_RATING_COMPONENTS:
        score = _get_reference_score(doctype, doc.get(source_field))
        doc.set(target_field, score)
        scores.append(score)
        notes.append(f"{doc.meta.get_label(source_field)}: {score}")

    country = _first_value(doc, COUNTRY_FIELDS)
    country_score = _get_country_score(country)
    doc.set("country_risk_score", country_score)
    scores.append(country_score)
    notes.append(f"Country/Jurisdiction: {country_score}")

    average = round(sum(scores) / len(scores), 2)
    doc.set("risk_score_average", average)
    doc.set("final_risk_rating", _rating_from_average(average))
    doc.set("risk_rating_notes", "\n".join(notes))


def _first_value(doc, fields):
    for field in fields:
        value = doc.get(field)
        if value:
            return value
    return None


def _get_reference_score(doctype, name):
    if not name:
        return 5
    return frappe.db.get_value(doctype, name, "risk_score") or 5


def _get_country_score(country):
    if not country:
        return 5
    return frappe.db.get_value("KYC Country Risk", {"country": country}, "risk_score") or 5


def _rating_from_average(average):
    if average <= 2:
        return "Low Risk"
    if average <= 3.5:
        return "Medium Risk"
    return "High Risk"
