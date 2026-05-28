import frappe
from fiaserve_ekyc.fiaserve_ekyc.utils.seed_data import COUNTRIES


def get_context(context):
	context.no_cache = 1
	context.title = "Individual KYC - FIASERV eKYC"
	context.countries = COUNTRIES
