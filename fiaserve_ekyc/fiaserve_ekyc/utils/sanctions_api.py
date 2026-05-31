"""
OpenSanctions API integration.
Docs: https://www.opensanctions.org/docs/api/
"""
from __future__ import annotations

import json
from datetime import datetime

import frappe
import requests

OPENSANCTIONS_MATCH_URL = "https://api.opensanctions.org/match/default"
OPENSANCTIONS_SEARCH_URL = "https://api.opensanctions.org/search/default"
DATA_FIELD_MAX_LENGTH = 140

SANCTIONS_LIST_NAMES = {
	"afdb": "African Development Bank Group",
	"adb": "Asian Development Bank",
	"eu_fsf": "European Union Financial Sanctions Files",
	"ofac_sdn": "Office of Foreign Assets Control Specially Designated Nationals",
	"un_sc": "United Nations Security Council Consolidated List",
	"worldbank": "World Bank Debarred Firms and Individuals",
}


def _get_headers():
	api_key = frappe.conf.get("opensanctions_api_key", "")
	headers = {"Accept": "application/json", "Content-Type": "application/json"}
	if api_key:
		headers["Authorization"] = f"ApiKey {api_key}"
	return headers


def _search_entity(name: str, schema: str = "Thing") -> dict:
	match_response = _match_entity(name, schema=schema)
	if _get_result_rows(match_response):
		return match_response

	search_response = _search_default(name, schema=schema)
	if _get_result_rows(search_response):
		return {
			"responses": {"customer": search_response},
			"source": "search/default fallback",
			"match_response": match_response,
		}

	return match_response if match_response else search_response


def _match_entity(name: str, schema: str = "Thing") -> dict:
	payload = {
		"queries": {
			"customer": {
				"schema": schema,
				"properties": {"name": [name]},
			}
		}
	}
	params = {"limit": 10, "threshold": 0.3}
	try:
		resp = requests.post(OPENSANCTIONS_MATCH_URL, params=params, json=payload, headers=_get_headers(), timeout=15)
		resp.raise_for_status()
		return resp.json()
	except requests.RequestException as exc:
		return _api_error_response(exc, "OpenSanctions Match API Error")


def _search_default(name: str, schema: str = "Thing") -> dict:
	params = {"q": name, "schema": schema, "limit": 10, "fuzzy": "true"}
	try:
		resp = requests.get(OPENSANCTIONS_SEARCH_URL, params=params, headers=_get_headers(), timeout=15)
		resp.raise_for_status()
		return resp.json()
	except requests.RequestException as exc:
		return _api_error_response(exc, "OpenSanctions Search API Error")


def _api_error_response(exc: requests.RequestException, title: str) -> dict:
	resp = getattr(exc, "response", None)
	error_response = {
		"error": str(exc),
		"status_code": getattr(resp, "status_code", None),
		"response_text": (getattr(resp, "text", "") or "")[:4000],
	}
	frappe.log_error(message=json.dumps(error_response, indent=2), title=title)
	return error_response


def _get_result_rows(api_response: dict) -> list:
	return api_response.get("responses", {}).get("customer", {}).get("results", api_response.get("results", []))


def _extract_matches(api_response: dict) -> list:
	matches = []
	results = _get_result_rows(api_response)
	for result in results:
		props = result.get("properties", {})
		topics = result.get("topics", [])
		names = _as_list(props.get("name")) or [result.get("caption", "")]
		matches.append({
			"entity_id": _as_data(result.get("id", "")),
			"entity_name": _as_data(_pick_display_name(result, names)),
			"match_score": result.get("score", 0.0),
			"datasets": _as_data(_format_dataset_names(result.get("datasets"))),
			"is_pep": 1 if "role.pep" in topics else 0,
			"is_sanctioned": 1 if any(topic in topics for topic in ["sanction", "sanction.linked", "debarment"]) else 0,
			"countries": _as_data(", ".join(_as_list(props.get("country", props.get("jurisdiction", []))))),
			"birth_date": _as_data(", ".join(_as_list(props.get("birthDate")))),
			"entity_url": _as_data(f"https://www.opensanctions.org/entities/{result.get('id', '')}"),
			"aliases_json": json.dumps(names, ensure_ascii=False, indent=2),
			"properties_json": json.dumps(props, indent=2),
		})
	return matches


def _format_dataset_names(value):
	return ", ".join(SANCTIONS_LIST_NAMES.get(item.lower(), item) for item in _as_list(value))


def _as_list(value):
	if value is None:
		return []
	if isinstance(value, list):
		return [str(item) for item in value if item is not None]
	return [str(value)]


def _as_data(value, max_length: int = DATA_FIELD_MAX_LENGTH):
	value = " ".join(str(value or "").split())
	if len(value) <= max_length:
		return value
	return value[: max_length - 1].rstrip() + "…"


def _pick_display_name(result: dict, names: list[str]) -> str:
	caption = result.get("caption")
	if caption:
		return caption

	for name in names:
		if name and name.isascii():
			return name

	for name in names:
		if name:
			return name

	return result.get("id", "")


def _determine_status(matches: list) -> str:
	if not matches:
		return "Clear"
	for match in matches:
		if match["is_sanctioned"] or match["is_pep"] or match["match_score"] >= 0.85:
			return "Match Found"
	return "Review Required"


def _save_screening(screening_doctype: str, link_field: str, customer_name_value: str, api_response: dict, matches: list, query: str):
	# Screening is now stored on the customer KYC record itself; keep this helper
	# signature for the existing callers while avoiding separate screening records.
	return "Review Required" if api_response.get("error") else _determine_status(matches)


def _get_total_results(api_response: dict, matches: list) -> int:
	response = api_response.get("responses", {}).get("customer", api_response)
	total = response.get("total", {})
	if isinstance(total, dict):
		return total.get("value") or len(matches)
	return len(matches)


def _update_customer_status(doctype: str, docname: str, status: str, api_response=None, matches=None, query=None):
	matches = matches or []
	pep_identified = any(match.get("is_pep") for match in matches)
	on_sanctions_list = any(match.get("is_sanctioned") for match in matches)
	pep_status = _get_pep_sanctions_status(pep_identified, on_sanctions_list)
	values = {
		"sanctions_status": status,
		"sanctions_screened_on": datetime.now(),
		"pep_identified": 1 if pep_identified else 0,
		"on_sanctions_list": 1 if on_sanctions_list else 0,
		"pep_sanctions_status": pep_status,
		"api_query": query,
		"match_found": 1 if matches else 0,
		"total_results": _get_total_results(api_response or {}, matches),
		"raw_api_response": json.dumps(api_response or {}, indent=2),
		"risk_assessment": status,
	}
	frappe.db.set_value(doctype, docname, values)
	doc = frappe.get_doc(doctype, docname)
	doc.flags._fiaserve_screening_started = True
	doc.set("matches_table", [dict({"doctype": "Sanctions Match Entry"}, **match) for match in matches])
	doc.save(ignore_permissions=True)
	frappe.db.commit()


def _get_pep_sanctions_status(pep_identified: bool, on_sanctions_list: bool):
	if pep_identified and on_sanctions_list:
		return "Screened, PEP identified, on Sanctions lists"
	if on_sanctions_list:
		return "Screened, PEP not identified, on Sanctions lists"
	if pep_identified:
		return "Screened, PEP identified, not on Sanctions lists"
	return "Screened, PEP not identified, not on Sanctions lists"


def _mark_screening_started(doc) -> bool:
	if getattr(doc.flags, "_fiaserve_screening_started", False):
		return False
	doc.flags._fiaserve_screening_started = True
	return True


def screen_individual(doc, method=None):
	if not _mark_screening_started(doc):
		return
	api_resp = _search_entity(doc.full_name, schema="Person")
	matches = _extract_matches(api_resp)
	status = _save_screening(None, "customer", doc.name, api_resp, matches, doc.full_name)
	_update_customer_status("Individual Customer", doc.name, status, api_resp, matches, doc.full_name)


def screen_high_risk_pep(doc, method=None):
	if not _mark_screening_started(doc):
		return
	api_resp = _search_entity(doc.full_name, schema="Person")
	matches = _extract_matches(api_resp)
	status = _save_screening(None, "customer", doc.name, api_resp, matches, doc.full_name)
	_update_customer_status("High Risk PEP Individual", doc.name, status, api_resp, matches, doc.full_name)


def screen_non_individual(doc, method=None):
	if not _mark_screening_started(doc):
		return
	api_resp = _search_entity(doc.entity_name, schema="Organization")
	matches = _extract_matches(api_resp)
	status = _save_screening(None, "customer", doc.name, api_resp, matches, doc.entity_name)
	_update_customer_status("Non-Individual Customer", doc.name, status, api_resp, matches, doc.entity_name)


def screen_high_risk_non_individual(doc, method=None):
	if not _mark_screening_started(doc):
		return
	api_resp = _search_entity(doc.entity_name, schema="Organization")
	matches = _extract_matches(api_resp)
	status = _save_screening(None, "customer", doc.name, api_resp, matches, doc.entity_name)
	_update_customer_status("High Risk Non-Individual", doc.name, status, api_resp, matches, doc.entity_name)


@frappe.whitelist()
def trigger_screening(doctype, docname):
	doc = frappe.get_doc(doctype, docname)
	dispatch = {
		"Individual Customer": screen_individual,
		"High Risk PEP Individual": screen_high_risk_pep,
		"Non-Individual Customer": screen_non_individual,
		"High Risk Non-Individual": screen_high_risk_non_individual,
	}
	fn = dispatch.get(doctype)
	if fn:
		fn(doc)
	return {"status": "Screening triggered"}
