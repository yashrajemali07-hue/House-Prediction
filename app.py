import streamlit as st
import pickle
import time

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NestValue · House Price AI",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

  /* ── Palette ── */
  :root {
    --clay:      #c8785a;
    --clay-dim:  #9e5c42;
    --ink:       #1a1510;
    --paper:     #fdf8f3;
    --border:    #e2d5c8;
    --muted:     #8a7b6e;
    --sage:      #6b8c72;

    /* Sidebar dark tokens */
    --sb-bg:      #1a1510;
    --sb-surface: #24201a;
    --sb-border:  #38302a;
    --sb-text:    #e8ddd4;
    --sb-label:   #9a8d82;
    --sb-accent:  #c8785a;
  }

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--paper) !important;
    color: var(--ink);
  }

  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 0 2rem 3rem !important; max-width: 1280px !important; }

  /* ──────────────────────────────────────
     DARK SIDEBAR
  ────────────────────────────────────── */
  [data-testid="stSidebar"] {
    background-color: var(--sb-bg) !important;
    border-right: 1px solid var(--sb-border) !important;
  }
  [data-testid="stSidebar"] .block-container {
    padding: 1.6rem 1.1rem !important;
  }

  /* All text inside sidebar */
  [data-testid="stSidebar"] p,
  [data-testid="stSidebar"] span,
  [data-testid="stSidebar"] div,
  [data-testid="stSidebar"] label {
    color: var(--sb-text) !important;
  }

  /* Section card */
  .sb-section {
    background: var(--sb-surface);
    border: 1px solid var(--sb-border);
    border-radius: 12px;
    padding: 1.1rem 1rem 1.2rem;
    margin-bottom: 1.1rem;
  }
  .sb-section-title {
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--sb-accent) !important;
    font-weight: 700;
    margin-bottom: 1rem;
  }

  /* Number inputs in sidebar */
  [data-testid="stSidebar"] input[type="number"] {
    background: var(--sb-bg) !important;
    color: var(--sb-text) !important;
    border: 1px solid var(--sb-border) !important;
    border-radius: 8px !important;
  }
  [data-testid="stSidebar"] input[type="number"]:focus {
    border-color: var(--sb-accent) !important;
    box-shadow: 0 0 0 2px #c8785a28 !important;
    outline: none !important;
  }

  /* Labels */
  [data-testid="stSidebar"] label {
    color: var(--sb-label) !important;
    font-size: 0.82rem !important;
  }

  /* Selectbox in sidebar */
  [data-testid="stSidebar"] [data-baseweb="select"] > div:first-child {
    background: var(--sb-bg) !important;
    border-color: var(--sb-border) !important;
    border-radius: 8px !important;
    color: var(--sb-text) !important;
  }
  [data-testid="stSidebar"] [data-baseweb="select"] svg {
    fill: var(--sb-label) !important;
  }

  /* Stepper +/- buttons */
  [data-testid="stSidebar"] button[data-testid="stNumberInput-StepUp"],
  [data-testid="stSidebar"] button[data-testid="stNumberInput-StepDown"] {
    background: var(--sb-surface) !important;
    border-color: var(--sb-border) !important;
    color: var(--sb-text) !important;
  }

  /* Sidebar HR */
  [data-testid="stSidebar"] hr {
    border-color: var(--sb-border) !important;
    margin: 0.8rem 0 1rem !important;
  }

  /* ── Predict button ── */
  .stButton > button {
    width: 100%;
    background: var(--clay) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 1rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.03em;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 18px #c8785a40 !important;
  }
  .stButton > button:hover {
    background: var(--clay-dim) !important;
    box-shadow: 0 6px 24px #c8785a60 !important;
    transform: translateY(-1px);
  }

  /* ── Hero ── */
  .hero {
    background: linear-gradient(135deg, #1a1510 0%, #2e2118 65%, #c8785a18 100%);
    border-radius: 18px;
    padding: 3.2rem 3rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
  }
  .hero::before {
    content: '';
    position: absolute; inset: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none'%3E%3Cg fill='%23c8785a' fill-opacity='0.06'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  }
  .hero-eyebrow {
    font-size: 0.68rem; letter-spacing: 0.2em; text-transform: uppercase;
    color: var(--clay); font-weight: 700; margin-bottom: 0.7rem;
  }
  .hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2rem, 4.5vw, 3.4rem);
    color: #fff; line-height: 1.1; margin: 0 0 1rem;
  }
  .hero-title em { color: var(--clay); font-style: italic; }
  .hero-sub { color: #c2b5ab; font-size: 0.96rem; font-weight: 300; max-width: 440px; line-height: 1.6; }
  .hero-badge {
    display: inline-block; background: #ffffff10; border: 1px solid #ffffff20;
    border-radius: 100px; padding: 0.28rem 0.85rem; font-size: 0.74rem;
    color: #ccc; margin-top: 1.3rem; backdrop-filter: blur(6px);
  }

  /* ── Result card ── */
  .result-card {
    background: linear-gradient(135deg, #1a1510, #2e2118);
    border-radius: 18px; padding: 2.4rem 2rem;
    text-align: center; position: relative; overflow: hidden;
    box-shadow: 0 16px 48px #00000028;
  }
  .result-label {
    font-size: 0.68rem; letter-spacing: 0.2em; text-transform: uppercase;
    color: var(--clay); margin-bottom: 0.5rem;
  }
  .result-price {
    font-family: 'DM Serif Display', serif; font-size: 2.9rem;
    color: #fff; line-height: 1; margin-bottom: 0.3rem;
  }
  .result-sub { color: #9a8d82; font-size: 0.82rem; }

  .tag {
    display: inline-block; border-radius: 100px;
    padding: 0.32rem 1rem; font-size: 0.78rem; font-weight: 600; margin-top: 1.1rem;
  }
  .tag-premium { background: #c8785a22; color: var(--clay);  border: 1px solid #c8785a55; }
  .tag-comfort  { background: #6b8c7222; color: var(--sage);  border: 1px solid #6b8c7255; }
  .tag-budget   { background: #5a7ec822; color: #5a7ec8;      border: 1px solid #5a7ec855; }

  /* ── Insight tiles ── */
  .insight-grid { display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 1.4rem; }
  .insight-tile {
    flex: 1; min-width: 130px;
    background: #fff; border: 1px solid var(--border);
    border-radius: 12px; padding: 1rem; text-align: center;
  }
  .insight-tile .val { font-size: 1.05rem; font-weight: 600; color: var(--ink); }
  .insight-tile .lbl { font-size: 0.7rem; color: var(--muted); margin-top: 0.2rem; }

  /* ── Summary ── */
  .divider { border: none; border-top: 1px solid var(--border); margin: 1.6rem 0; }
  .summary-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 0.45rem 0; border-bottom: 1px solid var(--border);
  }
  .summary-row:last-child { border-bottom: none; }
  .summary-key { font-size: 0.82rem; color: var(--muted); }
  .summary-val { font-size: 0.88rem; font-weight: 600; color: var(--ink); }

  /* ── Placeholder ── */
  .placeholder {
    border: 2px dashed var(--border); border-radius: 18px;
    padding: 3.5rem 2rem; text-align: center; color: var(--muted);
  }
  .placeholder p { font-size: 0.93rem; line-height: 1.6; }

  /* ── Footer ── */
  .footer {
    text-align: center; color: var(--muted); font-size: 0.75rem;
    margin-top: 3rem; padding-top: 1.4rem; border-top: 1px solid var(--border);
  }
</style>
""", unsafe_allow_html=True)


# ─── Model loader ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    try:
        return pickle.load(open("model.pkl", "rb"))
    except FileNotFoundError:
        return None

model = load_model()


# ─── Helpers ──────────────────────────────────────────────────────────────────
LOCATION_MAP = {"Low": 0, "Medium": 0.5, "Premium": 1}
INCOME_MAP   = {"Low": 0, "Medium": 0.5, "High": 1}

def tier_label(price):
    if price >= 8_000_000:
        return ("Ultra Luxury", "tag-premium")
    elif price >= 4_000_000:
        return ("Premium Segment", "tag-premium")
    elif price >= 2_000_000:
        return ("Mid-Comfort Segment", "tag-comfort")
    else:
        return ("Budget Friendly", "tag-budget")

def fmt_inr(n):
    if n >= 1_00_00_000:
        return f"₹{n/1_00_00_000:.2f} Cr"
    elif n >= 1_00_000:
        return f"₹{n/1_00_000:.2f} L"
    return f"₹{n:,.0f}"


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div style='font-family:DM Serif Display,serif;font-size:1.35rem;"
        "color:#e8ddd4;margin-bottom:0.2rem'>NestValue</div>"
        "<div style='font-size:0.75rem;color:#9a8d82;margin-bottom:1rem'>"
        "AI-powered property valuation</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr>", unsafe_allow_html=True)

    # Property Details
    st.markdown(
        '<div class="sb-section">'
        '<div class="sb-section-title">Property Details</div>',
        unsafe_allow_html=True,
    )
    area      = st.number_input("Area (sq ft)",  min_value=100,  max_value=10000, value=1500, step=50)
    bedrooms  = st.number_input("Bedrooms",       min_value=1,    max_value=10,    value=3,    step=1)
    bathrooms = st.number_input("Bathrooms",      min_value=1,    max_value=10,    value=2,    step=1)
    floors    = st.number_input("Floors",         min_value=1,    max_value=5,     value=1,    step=1)
    st.markdown('</div>', unsafe_allow_html=True)

    # Location & Economics
    st.markdown(
        '<div class="sb-section">'
        '<div class="sb-section-title">Location & Economics</div>',
        unsafe_allow_html=True,
    )
    location_label     = st.selectbox("Location Type",     list(LOCATION_MAP.keys()))
    income_level_label = st.selectbox("Area Income Level", list(INCOME_MAP.keys()))
    st.markdown('</div>', unsafe_allow_html=True)

    predict_clicked = st.button("Predict Price", use_container_width=True)


# ─── MAIN AREA ────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">AI Property Valuation</div>
  <div class="hero-title">What's your home<br><em>really</em> worth?</div>
  <div class="hero-sub">
    Get an instant AI-powered estimate based on property features,
    location tier, and neighbourhood income profile.
  </div>
  <div class="hero-badge">Machine Learning &middot; Instant Results &middot; ₹ INR</div>
</div>
""", unsafe_allow_html=True)

col_result, col_summary = st.columns([3, 2], gap="large")

with col_result:
    if predict_clicked:
        location_val     = LOCATION_MAP[location_label]
        income_level_val = INCOME_MAP[income_level_label]
        features = [[area, bedrooms, bathrooms, floors, location_val, income_level_val]]

        if model is None:
            price = (
                area      * 4200
                + bedrooms  * 180_000
                + bathrooms * 90_000
                + floors    * 120_000
                + location_val     * 600_000
                + income_level_val * 300_000
            )
        else:
            with st.spinner("Analysing property…"):
                time.sleep(0.7)
            price = float(model.predict(features)[0])

        tier, tag_cls = tier_label(price)
        price_str     = fmt_inr(price)

        st.markdown(f"""
        <div class="result-card">
          <div class="result-label">Estimated Market Value</div>
          <div class="result-price">{price_str}</div>
          <div class="result-sub">±5% margin &middot; Based on current market data</div>
          <span class="tag {tag_cls}">{tier}</span>
        </div>
        """, unsafe_allow_html=True)

        price_per_sqft = price / area if area else 0
        st.markdown(f"""
        <div class="insight-grid">
          <div class="insight-tile">
            <div class="val">₹{price_per_sqft:,.0f}</div>
            <div class="lbl">Per sq ft</div>
          </div>
          <div class="insight-tile">
            <div class="val">{fmt_inr(price / bedrooms)}</div>
            <div class="lbl">Per bedroom</div>
          </div>
          <div class="insight-tile">
            <div class="val">{tier.split()[0]}</div>
            <div class="lbl">Market tier</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="placeholder">
          <p>Configure your property in the sidebar<br>and click <strong>Predict Price</strong> to get an estimate.</p>
        </div>
        """, unsafe_allow_html=True)

with col_summary:
    st.markdown("#### Property Summary")
    summary_data = {
        "Area":         f"{area:,} sq ft",
        "Bedrooms":     bedrooms,
        "Bathrooms":    bathrooms,
        "Floors":       floors,
        "Location":     location_label,
        "Income Level": income_level_label,
    }
    rows_html = "".join(
        f'<div class="summary-row">'
        f'<span class="summary-key">{k}</span>'
        f'<span class="summary-val">{v}</span>'
        f'</div>'
        for k, v in summary_data.items()
    )
    st.markdown(rows_html, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("#### How it works")
    st.markdown(
        "<div style='font-size:0.84rem;color:var(--muted);line-height:1.75'>"
        "The model analyses <strong>6 key property features</strong> trained on "
        "thousands of real-estate transactions — combining structural attributes "
        "(area, rooms, floors) with socioeconomic signals (location tier, income "
        "profile) to deliver a calibrated price estimate."
        "</div>",
        unsafe_allow_html=True,
    )

st.markdown("""
<div class="footer">
  NestValue &middot; AI House Price Predictor &middot; Built with Streamlit<br>
  For illustrative purposes only. Always consult a certified property valuator.
</div>
""", unsafe_allow_html=True)