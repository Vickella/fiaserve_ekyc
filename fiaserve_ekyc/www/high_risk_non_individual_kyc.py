from fiaserve_ekyc.fiaserve_ekyc.utils.seed_data import COUNTRIES
from fiaserve_ekyc.www.portal_context import apply_portal_context


def get_context(context):
	apply_portal_context(context)
	context.title = "High Risk Non-Individual KYC - FIASERV eKYC"
	context.countries = COUNTRIES
