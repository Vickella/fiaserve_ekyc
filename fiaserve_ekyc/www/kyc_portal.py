from fiaserve_ekyc.www.portal_context import apply_portal_context


def get_context(context):
	apply_portal_context(context)
	context.title = "KYC Portal - FIASERV eKYC"
