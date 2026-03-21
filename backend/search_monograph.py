
import requests
import base64
import re
import os
from dotenv import load_dotenv
from summarize_monograph import summarize_monograph

load_dotenv()

HEADERS = {"User-Agent": "Mozilla/5.0"}


def get_drug_code(din: str) -> int | None:
    """DIN → drug_code via Health Canada DPD API."""
    r = requests.get(
        "https://health-products.canada.ca/api/drug/drugproduct/",
        params={"din": din, "lang": "en"},
        headers=HEADERS,
        timeout=10,
    )
    r.raise_for_status()
    data = r.json()
    if isinstance(data, list) and data:
        return data[0].get("drug_code")
    return None


def get_monograph_pdf_url(drug_code: int) -> str | None:
    """Fetch the DHPP resource page and extract the pdf.hres.ca link."""
    r = requests.get(
        f"https://dhpp.hpfb-dgpsa.ca/dhpp/resource/{drug_code}",
        headers=HEADERS,
        timeout=10,
    )
    r.raise_for_status()
    match = re.search(r"https://pdf\.hres\.ca/dpd_pm/\d+\.PDF", r.text, re.IGNORECASE)
    return match.group(0) if match else None


def fetch_pdf_base64(pdf_url: str) -> str:
    """Download PDF and return as base64 string."""
    r = requests.get(pdf_url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return base64.standard_b64encode(r.content).decode("utf-8")


def din_to_monograph(din: str) -> dict:
    drug_code = get_drug_code(din)
    if not drug_code:
        raise ValueError(f"DIN '{din}' not found in Health Canada database.")

    pdf_url = get_monograph_pdf_url(drug_code)
    if not pdf_url:
        raise ValueError(f"No monograph PDF found for DIN '{din}' (drug_code={drug_code}).")

    pdf_b64 = fetch_pdf_base64(pdf_url)

    return {
        "din":       din,
        "drug_code": drug_code,
        "pdf_url":   pdf_url,
        "pdf_b64":   pdf_b64,
    }


result = din_to_monograph("02549883")
print(result["din"])
print(result["drug_code"])
print(result["pdf_url"])
summary = summarize_monograph(result["pdf_url"])
print(summary)
print(f"PDF size: {len(result['pdf_b64'])} chars (base64)")