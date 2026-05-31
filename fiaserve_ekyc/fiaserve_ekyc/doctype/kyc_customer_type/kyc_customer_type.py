from frappe.model.document import Document


class KYCCustomerType(Document):
	pass


# Backward-compatible alias for tools/docs that PascalCase acronyms as `Kyc`.
class KycCustomerType(KYCCustomerType):
	pass
