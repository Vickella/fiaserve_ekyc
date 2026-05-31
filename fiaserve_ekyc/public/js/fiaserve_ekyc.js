const COUNTRIES = ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo (Brazzaville)", "Congo (Kinshasa)", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea (North)", "Korea (South)", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"];

function populateCountries(fieldIds) {
  fieldIds.forEach(id => {
    let sel = document.getElementById(id);
    if (!sel) return;
    if (sel.tagName !== "SELECT") {
      const replacement = document.createElement("select");
      replacement.id = sel.id;
      replacement.name = sel.name;
      replacement.required = sel.required;
      replacement.className = sel.className;
      replacement.dataset.previousValue = sel.value || "";
      sel.replaceWith(replacement);
      sel = replacement;
    }
    sel.innerHTML = '<option value="">-- Select --</option>';
    COUNTRIES.forEach(c => {
      const opt = document.createElement("option");
      opt.value = c;
      opt.textContent = c;
      sel.appendChild(opt);
    });
    if (sel.dataset.previousValue) sel.value = sel.dataset.previousValue;
  });
}

function toggleSection(sectionId, show) {
  const el = document.getElementById(sectionId);
  if (el) {
    el.style.display = show ? "block" : "none";
    el.querySelectorAll("input, select, textarea").forEach(field => {
      if (field.type !== "checkbox") field.required = !!show;
    });
  }
  const repDoc = document.getElementById("rep-doc-field");
  if (repDoc) {
    repDoc.style.display = show ? "block" : "none";
    repDoc.querySelectorAll("input, select, textarea").forEach(field => {
      field.required = !!show;
    });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const representativeCheckbox = document.getElementById("has_representative");
  hydratePortalLogos();
  if (!representativeCheckbox) return;

  toggleSection("rep-section", representativeCheckbox.checked);
  representativeCheckbox.addEventListener("change", () => {
    toggleSection("rep-section", representativeCheckbox.checked);
  });
});

function hydratePortalLogos() {
  document.querySelectorAll(".fias-brand img").forEach(img => {
    const markMissing = () => {
      img.style.display = "none";
      if (!img.parentElement.querySelector(".fias-logo-fallback")) {
        const fallback = document.createElement("span");
        fallback.className = "fias-logo-fallback";
        fallback.textContent = "FIAServ";
        img.insertAdjacentElement("afterend", fallback);
      }
    };
    img.addEventListener("error", markMissing);
    if (img.complete && img.naturalWidth === 0) markMissing();
  });
}

function showAlert(message, type = "info") {
  const el = document.getElementById("fias-alert");
  if (!el) return;
  el.className = `fias-alert ${type}`;
  el.innerHTML = message;
  el.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function getCsrfToken() {
  if (window.frappe && window.frappe.csrf_token && window.frappe.csrf_token !== "None") {
    return window.frappe.csrf_token;
  }
  const cookieToken = document.cookie.split("; ").find(r => r.startsWith("X-Frappe-CSRF-Token="));
  return cookieToken ? cookieToken.split("=")[1] : "";
}

async function callFiaservMethod(method, args) {
  const resp = await fetch(`/api/method/${method}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Frappe-CSRF-Token": getCsrfToken(),
    },
    body: JSON.stringify(args || {}),
  });
  const data = await resp.json().catch(() => ({}));
  if (!resp.ok || data.exc) {
    throw new Error(data._server_messages || data.exception || data.exc || resp.statusText || "Request failed");
  }
  return data.message;
}

async function uploadFile(file, doctype, docname, fieldname) {
  if (!file || !file.name) return null;
  const formData = new FormData();
  formData.append("file", file, file.name);
  formData.append("is_private", "1");
  formData.append("doctype", doctype);
  formData.append("docname", docname);
  formData.append("fieldname", fieldname);
  formData.append("folder", "Home/Attachments");
  const resp = await fetch("/api/method/upload_file", { method: "POST", headers: { "X-Frappe-CSRF-Token": getCsrfToken() }, body: formData });
  if (!resp.ok) return null;
  const data = await resp.json();
  return data.message?.file_url || null;
}

async function submitKYCForm(doctype) {
  const form = document.getElementById("kyc-form");
  if (!form) return;
  if (document.getElementById("principals-table-body") && !document.querySelector("#principals-table-body tr")) {
    showAlert("At least one director, shareholder, trustee, or beneficiary is required.", "error");
    return;
  }
  if (!form.checkValidity()) {
    form.reportValidity();
    return;
  }
  const saveBtn = form.querySelector(".fias-btn-primary");
  const indicator = document.getElementById("saving-indicator");
  saveBtn.disabled = true;
  if (indicator) indicator.style.display = "inline";
  showAlert("Saving KYC record...", "info");
  const doc = { doctype };
  const fileFields = [];
  Array.from(form.elements).forEach(el => {
    if (!el.name) return;
    if (el.type === "file") {
      if (el.files[0]) fileFields.push({ fieldname: el.name, file: el.files[0] });
    } else if (el.type === "checkbox") {
      doc[el.name] = el.checked ? 1 : 0;
    } else if (el.tagName !== "BUTTON") {
      doc[el.name] = el.value;
    }
  });
  const principalRows = collectPrincipals();
  if (principalRows.length) doc.principals_table = principalRows;
  let result;
  try {
    result = await callFiaservMethod("fiaserve_ekyc.fiaserve_ekyc.utils.kyc_submission.submit_kyc", {
      doctype,
      doc: JSON.stringify(doc),
    });
  } catch (err) {
    showAlert(`Failed to save record: ${err}`, "error");
    saveBtn.disabled = false;
    if (indicator) indicator.style.display = "none";
    return;
  }
  if (fileFields.length) {
    showAlert("Uploading documents...", "info");
    const uploadUpdates = {};
    for (const { fieldname, file } of fileFields) {
      const url = await uploadFile(file, doctype, result.name, fieldname);
      if (url) uploadUpdates[fieldname] = url;
    }
    if (Object.keys(uploadUpdates).length) {
      await callFiaservMethod("fiaserve_ekyc.fiaserve_ekyc.utils.kyc_submission.update_kyc_attachments", {
        doctype,
        docname: result.name,
        values: JSON.stringify(uploadUpdates),
      });
    }
  }
  const route = doctype.toLowerCase().replace(/\s+/g, "-");
  showAlert(`KYC record <strong>${result.name}</strong> saved successfully. Sanctions status: <strong>${result.sanctions_status || "Pending"}</strong>. Screening records: <strong>${result.screening_count || 0}</strong>. <a href="/app/${route}/${result.name}" style="color:#1a2e6e;font-weight:700;">View Record</a>`, "success");
  saveBtn.disabled = false;
  if (indicator) indicator.style.display = "none";
}

function collectPrincipals() {
  const table = document.getElementById("principals-table-body");
  if (!table) return [];
  const rows = [];
  table.querySelectorAll("tr").forEach(tr => {
    const row = { doctype: "NIC Principal" };
    tr.querySelectorAll("input, select").forEach(inp => { if (inp.name) row[inp.name] = inp.value; });
    if (row.principal_name) rows.push(row);
  });
  return rows;
}

function addPrincipalRow() {
  const tbody = document.getElementById("principals-table-body");
  if (!tbody) return;
  const tr = document.createElement("tr");
  tr.innerHTML = `
    <td><input type="text" name="principal_name" placeholder="Full name" required></td>
    <td><select name="role" required><option>Director</option><option>Shareholder</option><option>Trustee</option><option>Settlor</option><option>Beneficiary</option><option>Signatory</option><option>Other</option></select></td>
    <td><select name="id_type" required><option>National ID</option><option>Passport</option><option>Driver's Licence</option><option>Residence Permit</option><option>Work Permit</option><option>Other</option></select></td>
    <td><input type="text" name="id_number" placeholder="ID Number" required></td>
    <td><select name="nationality" required>${COUNTRIES.map(c => `<option>${c}</option>`).join("")}</select></td>
    <td><button type="button" onclick="this.closest('tr').remove()">Remove</button></td>
  `;
  tbody.appendChild(tr);
}

window.populateCountries = populateCountries;
window.toggleSection = toggleSection;
window.showAlert = showAlert;
window.uploadFile = uploadFile;
window.submitKYCForm = submitKYCForm;
window.collectPrincipals = collectPrincipals;
window.addPrincipalRow = addPrincipalRow;
