# summarize.py
import anthropic
import base64
import requests
import os
from dotenv import load_dotenv

load_dotenv()

claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

HEADERS = {"User-Agent": "Mozilla/5.0"}


def fetch_pdf_base64(pdf_url: str) -> str:
    """Download PDF from URL and return as base64 string."""
    r = requests.get(pdf_url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return base64.standard_b64encode(r.content).decode("utf-8")


def summarize_monograph(pdf_url: str) -> str:
    """Takes a pdf.hres.ca URL, fetches it, and returns a plain-language summary."""
    pdf_b64 = fetch_pdf_base64(pdf_url)

    response = claude.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_b64,
                    },
                },
                {
                    "type": "text",
                    "text": """This is a Health Canada product monograph. Summarize it in plain language.

Cover:
1. What this drug is and what it treats
2. How to take it (dose and timing)
3. Key warnings and who should NOT take it
4. Common side effects
5. Important drug interactions

Write at a grade 8 reading level. Be concise — 3 to 5 short paragraphs.
Do not give personalized medical advice.""",
                },
            ],
        }],
    )

    return response.content[0].text


# # test
# if __name__ == "__main__":
#     pdf_url = "https://pdf.hres.ca/dpd_pm/00081570.PDF"
#     summary = summarize_monograph(pdf_url)
#     print(summary)