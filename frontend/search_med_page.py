import streamlit as st
import requests

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Canadian Drug Lookup",
    page_icon="💊",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root & background ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #F4F1EB;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stDecoration"] { display: none; }
.block-container { padding-top: 3rem; max-width: 720px; }

/* ── Hero title ── */
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 3rem;
    color: #1A1A2E;
    line-height: 1.1;
    margin-bottom: 0.2rem;
}
.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    color: #6B6B80;
    font-weight: 300;
    margin-bottom: 2.5rem;
    letter-spacing: 0.01em;
}
.badge {
    display: inline-block;
    background: #1A1A2E;
    color: #F4F1EB;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    padding: 3px 10px;
    border-radius: 2px;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

/* ── Search box ── */
[data-testid="stTextInput"] input {
    background: #FFFFFF;
    border: 1.5px solid #D9D4C7;
    border-radius: 6px;
    font-family: 'DM Mono', monospace;
    font-size: 1rem;
    color: #1A1A2E;
    padding: 0.75rem 1rem;
}
[data-testid="stTextInput"] input:focus {
    border-color: #1A1A2E;
    box-shadow: 0 0 0 3px rgba(26,26,46,0.08);
}

/* ── Radio toggle ── */
[data-testid="stRadio"] label { font-size: 0.9rem; color: #1A1A2E; }
[data-testid="stRadio"] > div { gap: 1.5rem; }

/* ── Button ── */
.stButton > button {
    background: #1A1A2E;
    color: #F4F1EB;
    border: none;
    border-radius: 6px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 0.95rem;
    padding: 0.6rem 2rem;
    letter-spacing: 0.03em;
    transition: background 0.2s, transform 0.1s;
}
.stButton > button:hover {
    background: #2E2E52;
    transform: translateY(-1px);
}

/* ── Result card ── */
.result-card {
    background: #FFFFFF;
    border: 1px solid #E0DBD0;
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.result-card h3 {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem;
    color: #1A1A2E;
    margin: 0 0 0.2rem 0;
}
.din-chip {
    display: inline-block;
    background: #EEF0F8;
    border: 1px solid #C8CBE8;
    color: #3A3A6E;
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    padding: 2px 10px;
    border-radius: 20px;
    margin-bottom: 0.8rem;
    letter-spacing: 0.06em;
}
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem 1.5rem;
    margin-top: 0.7rem;
}
.info-item label {
    display: block;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #9999AA;
    font-weight: 500;
    margin-bottom: 1px;
}
.info-item span {
    font-size: 0.92rem;
    color: #1A1A2E;
    font-weight: 400;
}
.ingredients-section {
    margin-top: 1rem;
    padding-top: 0.8rem;
    border-top: 1px dashed #E0DBD0;
}
.ingredients-section h4 {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #9999AA;
    margin: 0 0 0.5rem 0;
}
.ingredient-pill {
    display: inline-block;
    background: #F4F1EB;
    border: 1px solid #D9D4C7;
    border-radius: 4px;
    padding: 3px 10px;
    font-size: 0.82rem;
    color: #3A3A3A;
    margin: 2px 3px 2px 0;
    font-family: 'DM Sans', sans-serif;
}

/* ── No results / error ── */
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: #9999AA;
    font-size: 0.95rem;
}
.divider {
    border: none;
    border-top: 1px solid #E0DBD0;
    margin: 2rem 0;
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

def render_card(drug):
    drug_code = drug.get("drug_code")
    brand = drug.get("brand_name", "Unknown")
    din = drug.get("drug_identification_number", "—")
    company = drug.get("company_name", "—")
    last_update = drug.get("last_update_date", "—")

    schedule = fetch_schedule(drug_code)
    form = fetch_form(drug_code)
    ingredients = fetch_ingredients(drug_code) if drug_code else []

    ingredient_html = ""
    if ingredients:
        pills = "".join(
            f'<span class="ingredient-pill">{i["ingredient_name"]} {i["strength"]} {i["strength_unit"]}</span>'
            for i in ingredients
        )
        ingredient_html = f"""
        <div class="ingredients-section">
            <h4>Active Ingredients</h4>
            {pills}
        </div>
        """

    st.markdown(f"""
    <div class="result-card">
        <h3>{brand}</h3>
        <span class="din-chip">DIN&nbsp;&nbsp;{din}</span>
        <div class="info-grid">
            <div class="info-item"><label>Company</label><span>{company}</span></div>
            <div class="info-item"><label>Drug Code</label><span>{drug_code}</span></div>
            <div class="info-item"><label>Schedule</label><span>{schedule}</span></div>
            <div class="info-item"><label>Dosage Form</label><span>{form}</span></div>
            <div class="info-item"><label>Last Updated</label><span>{last_update}</span></div>
        </div>
        {ingredient_html}
    </div>
    """, unsafe_allow_html=True)

# ── UI ─────────────────────────────────────────────────────────────────────────

st.markdown('<div class="badge">Health Canada · DPD API</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Canadian Drug<br><i>Lookup</i></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Search Health Canada\'s Drug Product Database by brand name or DIN.</div>', unsafe_allow_html=True)

# Search box
mode = st.radio("Search by", ["Brand Name", "DIN"], horizontal=True)
placeholder = "e.g. ADVIL, TYLENOL, LIPITOR" if mode == "Brand Name" else "e.g. 00326925"
query = st.text_input("", placeholder=placeholder, label_visibility="collapsed")

search = st.button("Search →")

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# Results
if search and query.strip():
    with st.spinner("Querying Health Canada DPD…"):
        if mode == "Brand Name":
            results = fetch_by_name(query.strip().upper())
        else:
            results = fetch_by_din(query.strip())

    if not results:
        st.markdown(f'<div class="empty-state">No results found for <b>{query}</b>.<br>Try a different spelling or check the DIN.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f"**{len(results)} result{'s' if len(results) != 1 else ''} found**")
        for drug in results[:10]:  # cap at 10 to avoid rate limits
            render_card(drug)
        if len(results) > 10:
            st.caption(f"Showing first 10 of {len(results)} results. Narrow your search for more specific results.")

elif search and not query.strip():
    st.warning("Please enter a search term.")

st.markdown("""
<div style="text-align:center; margin-top:3rem; font-size:0.75rem; color:#B0AAA0; font-family:'DM Mono',monospace;">
    Data sourced from Health Canada's Drug Product Database (DPD) · No medical advice implied
</div>
""", unsafe_allow_html=True)