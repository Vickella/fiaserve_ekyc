import frappe

INDUSTRIES = [
    ("ACCEPTING HOUSES", 3, "Medium"), ("ACCOUNTING", 3, "Medium"), ("AIR TRANSPORT", 1, "Low"),
    ("AMUSEMENT & CATERING", 1, "Low"), ("AUDITING", 3, "Medium"), ("BEER, WINE & SPIRITS", 1, "Low"),
    ("BETTING AND GAMBLING", 4, "High"), ("BEVERAGES", 1, "Low"), ("BROADCASTING", 1, "Low"),
    ("BUILDING CONTRACTORS", 1, "Low"), ("BUILDING SOCIETIES", 4, "High"), ("CHROME", 4, "High"),
    ("CIVIL ENGINEERING CONTRACTORS", 1, "Low"), ("CLOTHING/FOOTWEAR", 1, "Low"), ("COMMERCIAL BANKS", 3, "Medium"),
    ("DAIRY", 1, "Low"), ("DEPARTMENTAL STORES", 1, "Low"), ("DISCOUNT HOUSES", 3, "Medium"),
    ("EDUCATION", 1, "Low"), ("ENERGY", 2, "Low"), ("ENTERTAINMENT", 2, "Low"), ("FARMING", 1, "Low"),
    ("FERTILISERS INSECTICIDES PESTICIDES", 3, "Medium"), ("FINANCE", 3, "Medium"), ("FINANCIAL TECHNOLOGY", 4, "High"),
    ("FISHING", 2, "Low"), ("FORESTRY AND WILDLIFE", 1, "Low"), ("GOVERNMENT", 3, "Medium"),
    ("HORTICULTURE", 1, "Low"), ("HOSPITALITY", 2, "Low"), ("INDUSTRIAL AND HEAVY EQUIPMENT", 2, "Low"),
    ("INSURANCE COMPANIES", 3, "Medium"), ("INFORMATION TECHNOLOGY", 2, "Low"), ("LEGAL", 4, "High"),
    ("LIVESTOCK", 1, "Low"), ("LOCAL AUTHORITIES (INC MUNICIPAL)", 4, "High"), ("LOGISTICS AND TRANSPORTATION", 3, "Medium"),
    ("MANUFACTURING", 4, "High"), ("MEDICAL PROFESSIONS AND HEALTHCARE", 2, "Low"), ("MINING (OTHER)", 4, "High"),
    ("MINING HOUSES", 4, "High"), ("MINING PRECIOUS METALS", 4, "High"), ("MOTOR TRADE (CAR DEALERS)", 3, "Medium"),
    ("NON-PROFIT AND CHARITABLE", 4, "High"), ("PENSION & PROVIDENT FUNDS", 3, "Medium"), ("POULTRY", 1, "Low"),
    ("PRECIOUS STONES AND METALS", 4, "High"), ("PRINTING AND PUBLISHING", 1, "Low"), ("PROFESSIONAL SERVICES", 3, "Medium"),
    ("REAL ESTATE", 4, "High"), ("RETAILERS", 1, "Low"), ("ROAD HAULAGE", 1, "Low"), ("SALES AND MARKETING", 2, "Low"),
    ("SECURITY BROKERS & DEALERS", 3, "Medium"), ("SOAPS TOILETRIES & PHARMACEUTICALS", 2, "Low"), ("SPORTING", 3, "Medium"),
    ("TELECOMMUNICATIONS", 1, "Low"), ("TOBACCO", 3, "Medium"), ("TOURISM", 4, "High"),
    ("TRUST COMPANIES & EXECUTORS", 4, "High"), ("UNKNOWN", 5, "Auto High"), ("WHOLESALERS", 3, "Medium"),
]

OCCUPATIONS = [
    ("ACCOUNTANT", 2, "Low"), ("ACTUARY", 2, "Low"), ("ADMINISTRATOR", 1, "Low"), ("ADVOCATE", 3, "Medium"),
    ("AIRLINE CABIN STAFF", 4, "High"), ("AIRLINE PILOT", 3, "Medium"), ("AMBULANCE PERSON", 1, "Low"),
    ("AMUSEMENT & RECREATION", 3, "Medium"), ("ANAESTHETIST", 1, "Low"), ("ANALYST", 1, "Low"),
    ("ANIMAL FARMING OCCUPATIONS", 1, "Low"), ("APPRENTICE", 1, "Low"), ("ARCHITECT", 1, "Low"),
    ("ARTICLED CLERK", 1, "Low"), ("ARTISAN", 1, "Low"), ("ARTIST", 1, "Low"), ("ATTACHE FOR EMBASSY", 4, "High"),
    ("ATTORNEY", 4, "High"), ("AUDITOR", 3, "Medium"), ("BANKER", 2, "Low"), ("BOOKKEEPER", 2, "Low"),
    ("BOOKMAKER", 4, "High"), ("BROKER", 3, "Medium"), ("BUSINESS CONSULTANT", 2, "Low"), ("BUYER", 3, "Medium"),
    ("CASINO DEALER", 4, "High"), ("CHAIRMAN (EXEC)", 3, "Medium"), ("CHARTERED ACCOUNTANT", 3, "Medium"),
    ("CHEMICAL ENGINEER", 4, "High"), ("CHEMIST", 3, "Medium"), ("CIVIL SERVANT - EXECUTIVE", 4, "High"),
    ("COMMISSIONED OFFICER", 4, "High"), ("COMPANY SECRETARY (EXEC)", 3, "Medium"), ("CUSTOMS OFFICER", 5, "High"),
    ("DEFENSE FORCE", 5, "High"), ("DIRECTOR", 3, "Medium"), ("DOCTOR", 1, "Low"), ("DRIVER", 1, "Low"),
    ("ESTATE AGENT", 4, "High"), ("EXECUTIVE MANAGEMENT", 3, "Medium"), ("FARMER", 2, "Low"),
    ("FINANCIAL ADVISOR", 2, "Low"), ("GAME WARDEN", 3, "Medium"), ("GENERAL MANAGER (EXEC)", 3, "Medium"),
    ("HOUSEWIFE", 1, "Low"), ("IMPORT/EXPORT TRADER", 3, "Medium"), ("INSURANCE BROKER", 3, "Low"),
    ("JEWELLER", 4, "High"), ("JUDGE", 5, "High"), ("LAWYER", 4, "High"), ("MAGISTRATE", 5, "High"),
    ("MEMBER OF PARLIAMENT", 5, "High"), ("MINISTER OF RELIGION", 3, "Medium"), ("MINOR", 1, "Low"),
    ("NON WORKING", 2, "Low"), ("NURSE", 1, "Low"), ("PENSIONER", 1, "Low"), ("PILOT", 3, "Medium"),
    ("POLICE", 3, "Medium"), ("PRISON WARDER", 2, "Low"), ("PROFESSIONAL", 3, "Medium"),
    ("PROPERTY CONSULTANT", 3, "Medium"), ("SELF EMPLOYED", 3, "Medium"), ("SOLDIER", 3, "Medium"),
    ("SPECIALIST", 3, "Medium"), ("STOCKBROKER", 4, "High"), ("STUDENT", 1, "Low"),
    ("TAX CONSULTANT", 3, "Medium"), ("TAXI OWNER", 3, "Medium"), ("TEACHER", 1, "Low"),
    ("UNEMPLOYED", 2, "Low"), ("VETERINARIAN", 2, "Low"), ("ZOOLOGIST", 1, "Low"),
]

CUSTOMER_TYPES = [
    ("ASSOCIATION/SOCIETY", 2, "Low"), ("CLOSE CORPORATE", 1, "Low"), ("CLUBS", 2, "Low"),
    ("Cooperative Company", 3, "Medium"), ("CO-OPERATIVES", 3, "Medium"), ("CORRESPONDENT BANK", 4, "High"),
    ("EMBASSY & CONSULATE", 4, "High"), ("Estate", 3, "Medium"), ("ESTATE AC", 2, "Low"),
    ("Foreign Company", 3, "Medium"), ("FOREIGN NATIONALS", 3, "Medium"), ("Government (Agency)", 1, "Low"),
    ("Government (Consulate)", 1, "Low"), ("Government (Multinational/Regional Development Bank)", 1, "Low"),
    ("Government (Municipality)", 1, "Low"), ("Government (State-Owned Body)", 1, "Low"),
    ("INDIVIDUAL PERSON", 1, "Low"), ("LISTED/Public Limited Company (Recognised Stock Exchange)", 1, "Low"),
    ("MINOR CHILD", 1, "Low"), ("NON-LISTED COMPANY CLIENT", 2, "Low"), ("NON-PROFIT CO (NPC)", 4, "High"),
    ("OTHER LEGAL ENTITY", 2, "Low"), ("Partnership, Syndicate, Joint Ventures or Association", 2, "Low"),
    ("PARTNERSHIPS", 2, "Low"), ("Private Investment Company (PIC)", 5, "High"),
    ("Pvt Business Corporation/Sole Proprietary", 2, "Low"), ("Pvt Limited Company", 2, "Low"),
    ("RELIGIOUS BODY", 3, "Medium"), ("SPV, SPE, Special Investment Vehicle", 5, "High"),
    ("STATE OWNED ENTERPRISE", 4, "High"), ("TRUST INTER VIVOS", 4, "High"), ("TRUSTS", 4, "High"),
    ("UNKNOWN COMPANY TYPE", 5, "High"),
]

PEP_SANCTIONS_STATUSES = [
    ("Screened, PEP not identified, not on Sanctions lists", 1, "Minimal Risk"),
    ("Screened, PEP identified, not on Sanctions lists", 3, "Medium"),
    ("Screened, PEP not identified, on Sanctions lists", 5, "Auto High"),
    ("Screened, PEP identified, on Sanctions lists", 5, "Auto High"),
    ("Not Screened", 5, "High"),
]

COUNTRY_RISKS = [
    ("Afghanistan", 5, "High"), ("Albania", 5, "High"), ("Algeria", 5, "High"), ("American Samoa", 1, "Low"),
    ("Andorra", 5, "High"), ("Angola", 5, "High"), ("Anguilla", 3, "Medium"), ("Antarctica", 1, "Low"),
    ("Antigua and Barbuda", 3, "Medium"), ("Argentina", 3, "Medium"), ("Armenia", 1, "Low"), ("Australia", 1, "Low"),
    ("Austria", 1, "Low"), ("Azerbaijan", 5, "High"), ("Bahamas", 5, "High"), ("Bahrain", 3, "Medium"),
    ("Bangladesh", 3, "Medium"), ("Barbados", 5, "High"), ("Belarus", 5, "High"), ("Belgium", 1, "Low"),
    ("Belize", 5, "High"), ("Benin", 3, "Medium"), ("Bermuda", 3, "Medium"), ("Bhutan", 1, "Low"),
    ("Bolivia", 5, "High"), ("Bosnia and Herzegovina", 3, "Medium"), ("Botswana", 1, "Low"), ("Brazil", 3, "Medium"),
    ("Bulgaria", 5, "High"), ("Burkina Faso", 5, "High"), ("Burundi", 3, "Medium"), ("Cambodia", 5, "High"),
    ("Cameroon", 5, "High"), ("Canada", 1, "Low"), ("Cayman Islands", 5, "High"), ("Central African Republic", 5, "High"),
    ("Chad", 3, "Medium"), ("Chile", 1, "Low"), ("China", 3, "Medium"), ("Colombia", 5, "High"),
    ("Comoros", 3, "Medium"), ("Congo", 3, "Medium"), ("Congo (Democratic Republic)", 5, "High"),
    ("Costa Rica", 5, "High"), ("Croatia", 5, "High"), ("Cuba", 5, "High"), ("Cyprus", 5, "High"),
    ("Czech Republic", 1, "Low"), ("Denmark", 1, "Low"), ("Dominican Republic", 5, "High"), ("Ecuador", 5, "High"),
    ("Egypt", 5, "High"), ("El Salvador", 5, "High"), ("Eritrea", 5, "High"), ("Estonia", 1, "Low"),
    ("Ethiopia", 5, "High"), ("Finland", 1, "Low"), ("France", 1, "Low"), ("Germany", 1, "Low"),
    ("Ghana", 1, "Low"), ("Greece", 1, "Low"), ("Guatemala", 5, "High"), ("Guinea", 5, "High"),
    ("Haiti", 5, "High"), ("Honduras", 5, "High"), ("Hong Kong", 3, "Medium"), ("Hungary", 1, "Low"),
    ("India", 5, "High"), ("Indonesia", 5, "High"), ("Iran", 5, "Auto High"), ("Iraq", 5, "High"),
    ("Ireland", 1, "Low"), ("Israel", 1, "Low"), ("Italy", 1, "Low"), ("Jamaica", 5, "High"),
    ("Japan", 1, "Low"), ("Jordan", 5, "High"), ("Kazakhstan", 5, "High"), ("Kenya", 5, "High"),
    ("Korea (North)", 5, "Auto High"), ("Korea (South)", 3, "Medium"), ("Kuwait", 3, "Medium"),
    ("Lebanon", 5, "High"), ("Lesotho", 1, "Low"), ("Liberia", 5, "High"), ("Libya", 5, "High"),
    ("Luxembourg", 3, "Medium"), ("Malawi", 1, "Low"), ("Malaysia", 3, "Medium"), ("Mali", 5, "High"),
    ("Malta", 3, "Medium"), ("Mauritius", 3, "Medium"), ("Mexico", 5, "High"), ("Mozambique", 5, "High"),
    ("Myanmar", 5, "Auto High"), ("Namibia", 5, "High"), ("Netherlands", 1, "Low"), ("New Zealand", 1, "Low"),
    ("Nigeria", 5, "High"), ("Norway", 1, "Low"), ("Oman", 1, "Low"), ("Pakistan", 5, "High"),
    ("Panama", 5, "High"), ("Peru", 3, "Medium"), ("Philippines", 3, "Medium"), ("Poland", 1, "Low"),
    ("Portugal", 1, "Low"), ("Qatar", 1, "Low"), ("Romania", 1, "Low"), ("Russian Federation", 5, "High"),
    ("Rwanda", 1, "Low"), ("Saudi Arabia", 5, "High"), ("Senegal", 5, "High"), ("Serbia", 3, "Medium"),
    ("Seychelles", 3, "Medium"), ("Sierra Leone", 3, "Medium"), ("Singapore", 3, "Medium"), ("Slovakia", 1, "Low"),
    ("Slovenia", 1, "Low"), ("Somalia", 5, "High"), ("South Africa", 5, "High"), ("South Sudan", 5, "High"),
    ("Spain", 1, "Low"), ("Sri Lanka", 1, "Low"), ("Sudan", 5, "High"), ("Switzerland", 3, "Medium"),
    ("Syrian Arab Republic", 5, "High"), ("Taiwan", 1, "Low"), ("Tanzania", 5, "High"), ("Thailand", 1, "Low"),
    ("Togo", 3, "Medium"), ("Tunisia", 5, "High"), ("Turkey", 5, "High"), ("Uganda", 5, "High"),
    ("Ukraine", 5, "High"), ("United Arab Emirates", 5, "High"), ("United Kingdom", 1, "Low"),
    ("United States", 1, "Low"), ("Uruguay", 3, "Medium"), ("Venezuela", 5, "High"), ("Viet Nam", 5, "High"),
    ("Yemen", 5, "High"), ("Zambia", 1, "Low"), ("Zimbabwe", 1, "Low"),
]


def after_install():
    _seed_countries()
    _seed_reference_table("KYC Industry", "industry_name", INDUSTRIES)
    _seed_reference_table("KYC Occupation", "occupation_name", OCCUPATIONS)
    _seed_reference_table("KYC Customer Type", "customer_type_name", CUSTOMER_TYPES)
    _seed_reference_table("KYC PEP Sanctions Status", "owner_screening_status", PEP_SANCTIONS_STATUSES)
    _seed_country_risk()
    frappe.db.commit()


def _seed_countries():
    if not frappe.db.exists("DocType", "Country"):
        return
    for country, _, _ in COUNTRY_RISKS:
        if not frappe.db.exists("Country", country):
            frappe.get_doc({"doctype": "Country", "country_name": country}).insert(ignore_permissions=True)


def _seed_reference_table(doctype, name_field, rows):
    if not frappe.db.exists("DocType", doctype):
        return
    for label, score, rating in rows:
        if not frappe.db.exists(doctype, label):
            frappe.get_doc({
                "doctype": doctype,
                name_field: label,
                "risk_score": score,
                "rating": rating,
            }).insert(ignore_permissions=True)


def _seed_country_risk():
    if not frappe.db.exists("DocType", "KYC Country Risk"):
        return
    for country, score, rating in COUNTRY_RISKS:
        if not frappe.db.exists("KYC Country Risk", country):
            frappe.get_doc({
                "doctype": "KYC Country Risk",
                "country": country,
                "risk_score": score,
                "rating": rating,
            }).insert(ignore_permissions=True)
