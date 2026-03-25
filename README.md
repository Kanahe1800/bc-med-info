# BC Med Info

A simple application designed to help British Columbia residents determine whether specific prescription drugs are covered under BC health plans while also providing concise, reliable drug information sourced from Canadian government data.

# Overview

Healthcare information online is often fragmented and difficult to navigate. Our project aims to make reliable drug information more accessible by combining:

Drug coverage information from BC health plans
Official drug documentation from the Government of Canada
AI-assisted summaries to make complex medical documents easier to understand

By consolidating these sources into a single platform, users can quickly determine whether a drug is covered and understand important safety and usage information without navigating multiple government websites.

# How It Works
- A user searches for a drug.
- The application retrieves relevant data from the Canadian Government Drug and Health Products Portal.
- If a drug monograph exists, the PDF is processed and summarized using Claude.
- The application extracts and summarizes key sections: Section 4 (Dosage and Administration), Section 7 (Warnings and Precautions), and Section 11 (Storage, Stability)
- The summarized information is presented alongside drug coverage information for BC health plans.

**Impact Potential**

Misinformation and disinformation surrounding healthcare are increasingly common online. This project aims to provide a reliable and accessible source of information based strictly on government-approved data.

The platform is designed primarily for patients currently using prescription medications, helping them:

Understand what drugs their healthcare coverage includes
Access important safety and dosage information quickly
Avoid navigating multiple government websites

With further development, the platform could scale to include:

- Coverage information from other Canadian provinces 
- Expanded drug information databases
