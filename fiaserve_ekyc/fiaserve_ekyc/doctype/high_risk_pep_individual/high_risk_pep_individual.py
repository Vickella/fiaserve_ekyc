import frappe
from frappe.model.document import Document


class HighRiskPEPIndividual(Document):
	def before_save(self):
		if hasattr(self, "capture_date") and not self.capture_date:
			self.capture_date = frappe.utils.today()
		if hasattr(self, "kyc_officer") and not self.kyc_officer:
			self.kyc_officer = frappe.session.user

	def validate(self):
		if hasattr(self, "date_of_birth") and self.date_of_birth:
			if frappe.utils.date_diff(frappe.utils.today(), str(self.date_of_birth)) < 0:
				frappe.throw("Date of Birth cannot be in the future.")
