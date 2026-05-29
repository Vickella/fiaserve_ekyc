from . import __version__ as app_version

app_name = "fiaserve_ekyc"
app_title = "FIASERV eKYC"
app_publisher = "VerityCore Consultancy"
app_description = "Electronic Know-Your-Customer compliance platform"
app_email = "devs@veritycore.co.zw"
app_license = "MIT"
app_version = "1.0.0"

# The portal CSS/JS is loaded directly by the public KYC pages. Do not inject it
# into Desk, because it targets standard form classes used by ERPNext screens.
app_include_css = []
app_include_js = []

add_to_apps_screen = [
	{
		"name": "fiaserve_ekyc",
		"logo": "/assets/fiaserve_ekyc/images/fiaserv_logo.png",
		"title": "FIASERV eKYC",
		"route": "/app/fiaserve-ekyc",
		"has_permission": "fiaserve_ekyc.config.desktop.has_permission",
	}
]

after_install = "fiaserve_ekyc.fiaserve_ekyc.utils.seed_data.after_install"

doc_events = {
	"Individual Customer": {
		"after_insert": "fiaserve_ekyc.fiaserve_ekyc.utils.sanctions_api.screen_individual",
		"on_update": "fiaserve_ekyc.fiaserve_ekyc.utils.sanctions_api.screen_individual",
	},
	"High Risk PEP Individual": {
		"after_insert": "fiaserve_ekyc.fiaserve_ekyc.utils.sanctions_api.screen_high_risk_pep",
		"on_update": "fiaserve_ekyc.fiaserve_ekyc.utils.sanctions_api.screen_high_risk_pep",
	},
	"Non-Individual Customer": {
		"after_insert": "fiaserve_ekyc.fiaserve_ekyc.utils.sanctions_api.screen_non_individual",
		"on_update": "fiaserve_ekyc.fiaserve_ekyc.utils.sanctions_api.screen_non_individual",
	},
	"High Risk Non-Individual": {
		"after_insert": "fiaserve_ekyc.fiaserve_ekyc.utils.sanctions_api.screen_high_risk_non_individual",
		"on_update": "fiaserve_ekyc.fiaserve_ekyc.utils.sanctions_api.screen_high_risk_non_individual",
	},
}
