from fiaserve_ekyc.fiaserve_ekyc.utils.seed_data import COUNTRIES
from fiaserve_ekyc.fiaserve_ekyc.utils.risk_data import CUSTOMER_TYPES, INDUSTRIES, OCCUPATIONS
from fiaserve_ekyc.www.portal_context import apply_portal_context


def get_context(context):
	apply_portal_context(context)
	context.title = "Non-Individual KYC - FIASERV eKYC"
	context.countries = COUNTRIES
	context.industries = [row[0] for row in INDUSTRIES]
	context.occupations = [row[0] for row in OCCUPATIONS]
	context.customer_types = [row[0] for row in CUSTOMER_TYPES]
