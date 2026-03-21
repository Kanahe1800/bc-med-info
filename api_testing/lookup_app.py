import streamlit as st
import requests
from backend.search_med import search

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
/* Row 2 (fetch function result) — subtle blue tint to distinguish from row 1 */
.drug-table tbody tr.row-secondary {
    background: #F0F6FC;
    border-bottom: 2px solid #C5C0B5;
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

/* ── Ingredients section (below table) ── */
.ingredients-wrap {
    background: #FFFFFF;
    border: 1.5px solid #C5C0B5;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 1.2rem;
}
.ingredients-wrap h4 {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #4A4A5A;
    margin: 0 0 0.6rem 0;
}
/* Ingredient pill: #1A2E4A on #E6F1FB → 8.9:1 (AAA) */
.ingredient-pill {
    display: inline-block;
    background: #E6F1FB;
    border: 1px solid #8BAFD4;
    border-radius: 4px;
    padding: 3px 10px;
    font-size: 0.82rem;
    color: #1A2E4A;
    margin: 2px 3px 2px 0;
    font-family: 'DM Sans', sans-serif;
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

BASE_URL = "https://health-products.canada.ca/api/drug"

# ── API helpers ────────────────────────────────────────────────────────────────

def fetch_by_name(name):
    r = requests.get(f"{BASE_URL}/drugproduct/?brandname={name}&lang=en&type=json", timeout=10)
    return r.json() if r.status_code == 200 else None

def fetch_by_din(din):
    r = requests.get(f"{BASE_URL}/drugproduct/?din={din}&lang=en&type=json", timeout=10)
    return r.json() if r.status_code == 200 else None

def fetch_ingredients(drug_code):
    r = requests.get(f"{BASE_URL}/activeingredient/?id={drug_code}&lang=en&type=json", timeout=10)
    return r.json() if r.status_code == 200 else []

def fetch_schedule(drug_code):
    r = requests.get(f"{BASE_URL}/schedule/?id={drug_code}&lang=en&type=json", timeout=10)
    if r.status_code == 200 and r.json():
        return ", ".join(s.get("schedule_name", "") for s in r.json())
    return "—"

def fetch_form(drug_code):
    r = requests.get(f"{BASE_URL}/form/?id={drug_code}&lang=en&type=json", timeout=10)
    if r.status_code == 200 and r.json():
        return ", ".join(f.get("pharmaceutical_form_name", "") for f in r.json())
    return "—"

def is_din(query: str) -> bool:
    """DINs are 8-digit numeric codes. Treat any all-digit input as a DIN attempt."""
    return query.strip().isdigit()


def render_results_table(drugs):
    """
    Render a table with a header row + two data rows per drug.

    Row 1 — data from the original search result object.
    Row 2 — data returned by calling fetch_by_din(din) for the DIN column
             and fetch_by_name(brand_name) for the Name column on that same drug.

    Coverage and Special Authority Needed are left blank pending future data sources.
    """
    rows_html = ""
    for drug in drugs:
        # ── Row 1: values from the search result object ──
        din_val  = drug.get("drug_identification_number", "—")
        name_val = drug.get("brand_name", "—")

        # ── Row 2: values returned by the individual fetch functions ──
        # fetch_by_din returns a list; take the DIN from the first match.
        din_lookup = fetch_by_din(din_val) or []
        row2_din   = din_lookup[0].get("drug_identification_number", "—") if din_lookup else "—"

        # fetch_by_name returns a list; take the brand name from the first match.
        name_lookup = fetch_by_name(name_val) or []
        row2_name   = name_lookup[0].get("brand_name", "—") if name_lookup else "—"

        rows_html += f"""
        <tr>
            <td class="cell-din">{din_val}</td>
            <td>{name_val}</td>
            <td class="cell-blank">—</td>
            <td class="cell-blank">—</td>
        </tr>
        <tr class="row-secondary">
            <td class="cell-din">{row2_din}</td>
            <td>{row2_name}</td>
            <td class="cell-blank">—</td>
            <td class="cell-blank">—</td>
        </tr>
        """

    st.markdown(f"""
    <div class="drug-table-wrap">
        <table class="drug-table">
            <thead>
                <tr>
                    <th>DIN</th>
                    <th>Name</th>
                    <th>Coverage</th>
                    <th>Special Authority Needed</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)


def render_ingredients(drugs):
    """Render active ingredient pills for all returned drugs beneath the table."""
    for drug in drugs:
        drug_code = drug.get("drug_code")
        brand     = drug.get("brand_name", "Unknown")
        if not drug_code:
            continue

        ingredients = fetch_ingredients(drug_code)
        if not ingredients:
            continue

        pills = "".join(
            f'<span class="ingredient-pill">'
            f'{i["ingredient_name"]} {i["strength"]} {i["strength_unit"]}'
            f'</span>'
            for i in ingredients
        )
        st.markdown(f"""
        <div class="ingredients-wrap">
            <h4>Active Ingredients — {brand}</h4>
            {pills}
        </div>
        """, unsafe_allow_html=True)


# ── UI ─────────────────────────────────────────────────────────────────────────

st.markdown('<div class="badge">Health Canada · DPD API</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">British Columbia Drug<br><i>Lookup</i></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Search Health Canada\'s Drug Product Database by brand name or DIN.</div>', unsafe_allow_html=True)

query = st.text_input("", placeholder="Generic name or DIN", label_visibility="collapsed")

# Show auto-detect hint while the user types
if query.strip():
    if is_din(query.strip()):
        st.markdown('<span class="mode-chip mode-chip-din">🔢 Searching by DIN</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="mode-chip mode-chip-name">🔤 Searching by brand name</span>', unsafe_allow_html=True)

search = st.button("Search →")

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ── Results ────────────────────────────────────────────────────────────────────
if search and query.strip():
    # with st.spinner("Querying Health Canada DPD…"):
    #     if is_din(query.strip()):
    #         results = fetch_by_din(query.strip())
    #     else:
    #         results = fetch_by_name(query.strip().upper())

    # if not results:
    #     st.markdown(
    #         f'<div class="empty-state">No results found for <b>{query}</b>.'
    #         f'<br>Try a different spelling or check the DIN.</div>',
    #         unsafe_allow_html=True,
    #     )
    # else:
    #     display = results[:10]
    #     st.markdown(f"**{len(results)} result{'s' if len(results) != 1 else ''} found**")
    #     render_results_table(display)
    #     render_ingredients(display)
    #     if len(results) > 10:
    #         st.caption(
    #             f"Showing first 10 of {len(results)} results. "
    #             f"Narrow your search for more specific results."
    #         )
    st.markdown(query)
    st.markdown(type(query))
    search(query)

elif search and not query.strip():
    st.warning("Please enter a search term.")

st.markdown("""
<div class="footer-note">
    Data sourced from Health Canada's Drug Product Database and BC PharmaCare Formulary's Database · No medical advice implied
</div>
""", unsafe_allow_html=True)