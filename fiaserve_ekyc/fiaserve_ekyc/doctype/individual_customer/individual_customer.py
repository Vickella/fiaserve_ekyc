from frappe.model.document import Document

from fiaserve_ekyc.fiaserve_ekyc.utils.risk_rating import apply_risk_rating


class IndividualCustomer(Document):
    def validate(self):
        apply_risk_rating(self)
