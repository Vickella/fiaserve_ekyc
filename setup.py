from setuptools import find_packages, setup


setup(
	name="fiaserve_ekyc",
	version="1.0.0",
	description="FIASERV eKYC - Electronic KYC compliance platform",
	author="VerityCore Consultancy",
	author_email="devs@veritycore.co.zw",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=["frappe", "requests"],
)
