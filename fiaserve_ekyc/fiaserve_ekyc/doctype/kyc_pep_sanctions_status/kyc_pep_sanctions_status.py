from frappe.model.document import Document


class KYCPEPSanctionsStatus(Document):
	pass


# Backward-compatible alias for tools/docs that PascalCase acronyms as `Kyc`.
class KycPepSanctionsStatus(KYCPEPSanctionsStatus):
	pass
