"""
OpenSanctions API integration.
Docs: https://www.opensanctions.org/docs/api/
"""
from __future__ import annotations

import json
from datetime import datetime

import frappe
import requests

OPENSANCTIONS_BASE_URL = "https://api.opensanctions.org"


def _get_headers():
	api_key = frappe.conf.get("opensanctions_api_key", "")
	headers = {"Accept": "application/json"}
	if api_key:
		headers["Authorization"] = f"ApiKey {api_key}"
	return headers


def _search_entity(name: str, schema: str = "Thing") -> dict:
	params = {"q": name, "schema": schema, "limit": 10, "fuzzy": "true"}
	try:
		resp = requests.get(f"{OPENSANCTIONS_BASE_URL}/search/default", params=params, headers=_get_headers(), timeout=15)
		resp.raise_for_status()
		return resp.json()
	except Exception as exc:
		frappe.log_error(message=str(exc), title="OpenSanctions API Error")
		return {}


def _extract_matches(api_response: dict) -> list:
	matches = []
	for result in api_response.get("results", []):
		props = result.get("properties", {})
		topics = result.get("topics", [])
		matches.append({
			"entity_id": result.get("id", ""),
			"entity_name": ", ".join(props.get("name", [result.get("caption", "")])),
			"match_score": result.get("score", 0.0),
			"datasets": ", ".join(result.get("datasets", [])),
			"is_pep": 1 if "role.pep" in topics else 0,
			"is_sanctioned": 1 if any(topic in topics for topic in ["sanction", "sanction.linked", "debarment"]) else 0,
			"countries": ", ".join(props.get("country", props.get("jurisdiction", []))),
			"birth_date": ", ".join(props.get("birthDate", [])),
			"entity_url": f"https://www.opensanctions.org/entities/{result.get('id', '')}",
			"properties_json": json.dumps(props, indent=2),
		})
	return matches


def _determine_status(matches: list) -> str:
	if not matches:
		return "Clear"
	for match in matches:
		if match["is_sanctioned"] or match["is_pep"] or match["match_score"] >= 0.85:
			return "Match Found"
	return "Review Required"


def _save_screening(screening_doctype: str, link_field: str, customer_name_value: str, api_response: dict, matches: list, query: str):
	status = _determine_status(matches)
	doc = frappe.get_doc({
		"doctype": screening_doctype,
		link_field: customer_name_value,
		"screened_on": datetime.now(),
		"api_query": query,
		"match_found": 1 if matches else 0,
		"total_results": api_response.get("total", {}).get("value", len(matches)),
		"raw_api_response": json.dumps(api_response, indent=2),
		"matches_table": [dict({"doctype": "Sanctions Match Entry"}, **match) for match in matches],
		"risk_assessment": status,
	})
	doc.insert(ignore_permissions=True)
	frappe.db.commit()
	return status


def _update_customer_status(doctype: str, docname: str, status: str):
	frappe.db.set_value(doctype, docname, {"sanctions_status": status, "sanctions_screened_on": datetime.now()})
	frappe.db.commit()


def screen_individual(doc, method=None):
	api_resp = _search_entity(doc.full_name, schema="Person")
	matches = _extract_matches(api_resp)
	status = _save_screening("Individual Sanctions Screening", "customer", doc.name, api_resp, matches, doc.full_name)
	_update_customer_status("Individual Customer", doc.name, status)


def screen_high_risk_pep(doc, method=None):
	api_resp = _search_entity(doc.full_name, schema="Person")
	matches = _extract_matches(api_resp)
	status = _save_screening("High Risk PEP Sanctions Screening", "customer", doc.name, api_resp, matches, doc.full_name)
	_update_customer_status("High Risk PEP Individual", doc.name, status)


def screen_non_individual(doc, method=None):
	api_resp = _search_entity(doc.entity_name, schema="Organization")
	matches = _extract_matches(api_resp)
	status = _save_screening("Non-Individual Sanctions Screening", "customer", doc.name, api_resp, matches, doc.entity_name)
	_update_customer_status("Non-Individual Customer", doc.name, status)


def screen_high_risk_non_individual(doc, method=None):
	api_resp = _search_entity(doc.entity_name, schema="Organization")
	matches = _extract_matches(api_resp)
	status = _save_screening("High Risk Non-Individual Sanctions Screening", "customer", doc.name, api_resp, matches, doc.entity_name)
	_update_customer_status("High Risk Non-Individual", doc.name, status)


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
