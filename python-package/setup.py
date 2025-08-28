from pathlib import Path
from setuptools import setup, find_packages

cwd = Path(__file__).resolve().parent
requirements_file = cwd / "employee_events" / "requirements.txt"
requirements = requirements_file.read_text().splitlines() if requirements_file.exists() else []

setup(
    name="employee_events",
    version="0.1.0",
    description="SQL Query API",
    author="Daniel Rodríguez Ruiz",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["employee_events.db", "requirements.txt"],
    },
    install_requires=requirements,
    python_requires=">=3.8",
)