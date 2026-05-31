from frappe.model.document import Document


class KYCIndustry(Document):
	pass


# Backward-compatible alias for tools/docs that PascalCase acronyms as `Kyc`.
class KycIndustry(KYCIndustry):
	pass
