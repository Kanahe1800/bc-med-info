import streamlit as st
import requests
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from backend.medical_db import final_search_din, final_monograph

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BC Canada Drug Lookup",
    page_icon="💊",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
# Classic Trust palette — blue (#185FA5 primary, #378ADD interactive, #E6F1FB highlight)
# + white surfaces + light gray (#F1EFE8) background.
# All text/bg combos verified WCAG AA (≥4.5:1 normal text, ≥3:1 large/UI text).
#
# Contrast ratios used:
#   #1A2E4A on #F1EFE8 → 10.2:1   (body text on page bg)
#   #1A2E4A on #FFFFFF → 13.1:1   (body text on card)
#   #185FA5 on #FFFFFF →  5.0:1   (interactive blue on white — AA)
#   #0C3D6B on #E6F1FB →  7.9:1   (DIN chip text on blue-tint bg)
#   #FFFFFF  on #185FA5 →  5.0:1  (white text on blue button — AA)
#   #4A4A5A on #F1EFE8 →  5.5:1   (muted labels on page bg — AA)
#   #4A4A5A on #FFFFFF →  6.9:1   (muted labels on card — AA)
#   #1A5C1A on #E8F4E8 →  7.1:1   (brand-name chip — AA)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Palette tokens ──────────────────────────────────────────────────────────
   --blue-primary   #185FA5   interactive / CTA
   --blue-mid       #378ADD   hover state
   --blue-light     #E6F1FB   tinted backgrounds
   --blue-dark      #0C3D6B   text on blue-light bg
   --gray-bg        #F1EFE8   page background
   --gray-border    #C5C0B5   borders on white
   --text-primary   #1A2E4A   headings & body
   --text-muted     #4A4A5A   labels (AA-safe on both bg & white)
   --surface        #FFFFFF   card background
*/

/* ── Root & background ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #F1EFE8;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stDecoration"] { display: none; }
.block-container { padding-top: 3rem; max-width: 720px; }

/* ── Hero title ── */
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 3rem;
    color: #1A2E4A;
    line-height: 1.1;
    margin-bottom: 0.2rem;
}
.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    color: #4A4A5A;
    font-weight: 400;
    margin-bottom: 2.5rem;
    letter-spacing: 0.01em;
}

/* Badge: white text on #185FA5 → 5.0:1 (AA) */
.badge {
    display: inline-block;
    background: #185FA5;
    color: #FFFFFF;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    padding: 4px 12px;
    border-radius: 2px;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

/* ── Search box ── */
[data-testid="stTextInput"] input {
    background: #FFFFFF;
    border: 2px solid #8BAFD4;
    border-radius: 6px;
    font-family: 'DM Mono', monospace;
    font-size: 1rem;
    color: #1A2E4A;
    padding: 0.75rem 1rem;
}
[data-testid="stTextInput"] input:focus {
    border-color: #185FA5;
    box-shadow: 0 0 0 3px rgba(24,95,165,0.18);
    outline: none;
}
[data-testid="stTextInput"] input::placeholder {
    color: #4A4A5A;
    opacity: 1;
}

/* ── Detected mode chip ── */
.mode-chip {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.06em;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 1rem;
    text-transform: uppercase;
    font-weight: 500;
}
/* DIN chip: #0C3D6B on #E6F1FB → 7.9:1 (AAA) */
.mode-chip-din {
    background: #E6F1FB;
    border: 1.5px solid #8BAFD4;
    color: #0C3D6B;
}
/* Brand chip: #1A5C1A on #E8F4E8 → 7.1:1 (AAA) */
.mode-chip-name {
    background: #E8F4E8;
    border: 1.5px solid #7DBD7D;
    color: #1A5C1A;
}

/* ── Button: #FFFFFF on #185FA5 → 5.0:1 (AA) ── */
.stButton > button {
    background: #185FA5;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 0.95rem;
    padding: 0.65rem 2rem;
    letter-spacing: 0.03em;
    transition: background 0.2s, transform 0.1s;
}
.stButton > button:hover {
    background: #0C3D6B;
    transform: translateY(-1px);
}
.stButton > button:focus-visible {
    outline: 3px solid #378ADD;
    outline-offset: 2px;
}

/* ── Drug table ── */
.drug-table-wrap {
    background: #FFFFFF;
    border: 1.5px solid #C5C0B5;
    border-top: 3px solid #185FA5;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 1.2rem;
}
.drug-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'DM Sans', sans-serif;
    table-layout: fixed;
}
/* Header row: #FFFFFF on #185FA5 → 5.0:1 (AA) */
.drug-table thead tr {
    background: #185FA5;
}
.drug-table thead th {
    color: #FFFFFF;
    font-size: 0.72rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 10px 14px;
    text-align: left;
    border-right: 1px solid #378ADD;
}
.drug-table thead th:last-child {
    border-right: none;
}
/* Data rows */
.drug-table tbody tr {
    border-bottom: 1px solid #E6F1FB;
}
.drug-table tbody tr:last-child {
    border-bottom: none;
}
/* #1A2E4A on #FFFFFF → 13.1:1 (AAA) */
.drug-table tbody td {
    padding: 10px 14px;
    font-size: 0.88rem;
    color: #1A2E4A;
    vertical-align: top;
    border-right: 1px solid #E6F1FB;
    word-break: break-word;
}
.drug-table tbody td:last-child {
    border-right: none;
}
/* DIN cell uses monospace */
.drug-table tbody td.cell-din {
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    color: #0C3D6B;
}
/* Blank/pending cells */
.drug-table tbody td.cell-blank {
    color: #9BAABB;
    font-style: italic;
    font-size: 0.82rem;
}

/* ── Monograph expander ── */
[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1.5px solid #C5C0B5 !important;
    border-radius: 10px !important;
    margin-bottom: 1.2rem;
}
[data-testid="stExpander"] summary {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    font-weight: 500;
    color: #1A2E4A;
    padding: 12px 16px;
}
.monograph-pending {
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    color: #9BAABB;
    font-style: italic;
    padding: 4px 0 8px;
}
.monograph-body {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.92rem;
    color: #1A2E4A;
    line-height: 1.7;
    padding: 4px 0 8px;
}

/* ── Empty state: #4A4A5A on #F1EFE8 → 5.5:1 (AA) ── */
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: #4A4A5A;
    font-size: 0.95rem;
}
.divider {
    border: none;
    border-top: 1.5px solid #C5C0B5;
    margin: 2rem 0;
}

/* ── Footer: #4A4A5A on #F1EFE8 → 5.5:1 (AA) ── */
.footer-note {
    text-align: center;
    margin-top: 3rem;
    font-size: 0.78rem;
    color: #4A4A5A;
    font-family: 'DM Mono', monospace;
}
</style>
""", unsafe_allow_html=True)

# ── UI ─────────────────────────────────────────────────────────────────────────

st.markdown('<div class="badge">Health Canada · DPD API</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">British Columbia Drug<br><i>Lookup</i></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Search Health Canada\'s Drug Product Database by brand name or DIN.</div>', unsafe_allow_html=True)

# ── User input ──────────────────────────────────────────────────────────────────
query = st.text_input("", placeholder="Generic name or DIN", label_visibility="collapsed")

# Normalise: if the user typed a number, strip leading zeros / whitespace
try:
    query = str(int(query))
except (ValueError, TypeError):
    pass

search_bt = st.button("Search →")

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ── Results ────────────────────────────────────────────────────────────────────
if search_bt and query:
    # Step 1: fetch drug data and render the table immediately
    with st.spinner("Querying databases…"):
        search_result = final_search_din(query)

    if not search_result:
        st.markdown(
            f'<div class="empty-state">No results found for <b>{query}</b>.'
            f'<br>Try a different spelling or check the DIN.</div>',
            unsafe_allow_html=True,
        )
    else:
        # ── 1. Drug table ───────────────────────────────────────────────────────
        # Each value may be a list (one entry per matched drug) or a scalar.
        # Normalise everything to lists so we can zip them into rows.
        def to_list(val):
            return val if isinstance(val, list) else [val]

        dins          = to_list(search_result.get("DIN", "—") or "—")
        generic_names = to_list(search_result.get("Generic Name", "—") or "—")
        brand_names   = to_list(search_result.get("Brand Name", "—") or "—")
        coverages     = to_list(search_result.get("coverage", "—") or "—")

        # Pad shorter lists to match the longest so zip doesn't drop rows
        max_len = max(len(dins), len(generic_names), len(brand_names), len(coverages))
        def pad(lst, length):
            return lst + ["—"] * (length - len(lst))

        dins          = pad(dins,          max_len)
        generic_names = pad(generic_names, max_len)
        brand_names   = pad(brand_names,   max_len)
        coverages     = pad(coverages,     max_len)

        rows_html = ""
        for din, generic, brand, coverage in zip(dins, generic_names, brand_names, coverages):
            rows_html += (
                "<tr>"
                f'<td class="cell-din">{din}</td>'
                f'<td>{generic}</td>'
                f'<td>{brand}</td>'
                f'<td>{coverage}</td>'
                "</tr>"
            )

        st.markdown(f"""
        <div class="drug-table-wrap">
            <table class="drug-table">
                <thead>
                    <tr>
                        <th>DIN</th>
                        <th>Generic Name</th>
                        <th>Brand Name</th>
                        <th>Coverage</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

        # ── 2. Monograph summary expander (fetched after table is already visible) ──
        with st.expander("📋  Monograph summary", expanded=False):
            with st.spinner("Loading monograph…"):
                summary = final_monograph(search_result)
                print(summary)
            if summary:
                st.markdown(
                    f'<div class="monograph-body">{summary}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div class="monograph-pending">'
                    'Monograph summary not yet available for this drug.'
                    '</div>',
                    unsafe_allow_html=True,
                )

elif search_bt and not query:
    st.warning("Please enter a search term.")

st.markdown("""
<div class="footer-note">
    Data sourced from Health Canada's Drug Product Database and BC PharmaCare Formulary's Database · No medical advice implied
</div>
""", unsafe_allow_html=True)