from frappe import _


def get_data():
	return [
		{
			"module_name": "FIASERVE EKYC",
			"color": "#1a2e6e",
			"icon": "fa fa-id-card",
			"type": "module",
			"label": _("FIASERV eKYC"),
			"items": [
				{"type": "page", "name": "kyc_portal", "label": _("KYC Portal"), "icon": "fa fa-home", "description": "Start a new KYC capture"},
				{"type": "doctype", "name": "Individual Customer", "label": _("Individual Customers"), "icon": "fa fa-user"},
				{"type": "doctype", "name": "High Risk PEP Individual", "label": _("High Risk / PEP Individuals"), "icon": "fa fa-exclamation-triangle"},
				{"type": "doctype", "name": "Non-Individual Customer", "label": _("Non-Individual Customers"), "icon": "fa fa-building"},
				{"type": "doctype", "name": "High Risk Non-Individual", "label": _("High Risk Non-Individuals"), "icon": "fa fa-shield"},
				{"type": "doctype", "name": "Individual Sanctions Screening", "label": _("Individual Sanctions"), "icon": "fa fa-search"},
				{"type": "doctype", "name": "High Risk PEP Sanctions Screening", "label": _("PEP Sanctions"), "icon": "fa fa-search"},
				{"type": "doctype", "name": "Non-Individual Sanctions Screening", "label": _("Non-Individual Sanctions"), "icon": "fa fa-search"},
				{"type": "doctype", "name": "High Risk Non-Individual Sanctions Screening", "label": _("High Risk NI Sanctions"), "icon": "fa fa-search"},
			],
		}
	]


def has_permission():
	return True
