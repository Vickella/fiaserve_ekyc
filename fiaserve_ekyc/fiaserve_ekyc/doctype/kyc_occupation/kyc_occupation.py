from frappe.model.document import Document


class KYCOccupation(Document):
	pass


# Backward-compatible alias for tools/docs that PascalCase acronyms as `Kyc`.
class KycOccupation(KYCOccupation):
	pass
