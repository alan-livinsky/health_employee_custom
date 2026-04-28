from pathlib import Path

from setuptools import setup


MODULE_NAME = "z_health_employee_custom"
PACKAGE_NAME = f"trytond.modules.{MODULE_NAME}"
BASE_DIR = Path(__file__).parent


setup(
    name="trytond-z-health-employee-custom",
    version="6.0.0",
    description="Custom Tryton module to extend company.employee.",
    long_description=(BASE_DIR / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="Local customization",
    python_requires=">=3.10",
    packages=[PACKAGE_NAME],
    package_dir={PACKAGE_NAME: "."},
    package_data={
        PACKAGE_NAME: [
            "tryton.cfg",
            "company.xml",
            "report.txt",
            "view/*.xml",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "trytond>=6.0,<6.1",
        "trytond_company>=6.0,<6.1",
    ],
    entry_points={
        "trytond.modules": [
            f"{MODULE_NAME} = {PACKAGE_NAME}",
        ],
    },
)
