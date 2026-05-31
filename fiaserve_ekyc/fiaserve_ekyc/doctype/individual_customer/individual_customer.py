from frappe.model.document import Document

from fiaserve_ekyc.fiaserve_ekyc.utils.risk_rating import calculate_customer_risk


class IndividualCustomer(Document):
	def validate(self):
		calculate_customer_risk(self)
