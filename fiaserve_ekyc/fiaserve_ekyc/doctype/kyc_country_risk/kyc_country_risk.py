from frappe.model.document import Document


class KYCCountryRisk(Document):
	pass


# Backward-compatible alias for tools/docs that PascalCase acronyms as `Kyc`.
class KycCountryRisk(KYCCountryRisk):
	pass
