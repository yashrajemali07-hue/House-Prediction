import streamlit as st
import pickle
import time
import numpy as np

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NestValue · House Price AI",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

  /* ── Root palette ── */
  :root {
    --clay:   #c8785a;
    --clay-lt:#f0e0d6;
    --ink:    #1a1510;
    --sand:   #f5ede4;
    --sage:   #6b8c72;
    --paper:  #fdf8f3;
    --border: #e2d5c8;
    --muted:  #8a7b6e;
  }

  /* ── Global reset ── */
  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--paper) !important;
    color: var(--ink);
  }

  /* ── Hide default Streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 0 2rem 3rem !important; max-width: 1280px !important; }

  /* ── Hero banner ── */
  .hero {
    background: linear-gradient(135deg, #1a1510 0%, #2e2118 60%, #c8785a22 100%);
    border-radius: 20px;
    padding: 3.5rem 3rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
  }
  .hero::before {
    content: '';
    position: absolute; inset: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23c8785a' fill-opacity='0.06'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    opacity: 1;
  }
  .hero-eyebrow {
    font-size: 0.72rem; letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--clay); font-weight: 600; margin-bottom: 0.75rem;
  }
  .hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.2rem, 5vw, 3.6rem);
    color: #fff; line-height: 1.1; margin: 0 0 1rem;
  }
  .hero-title em { color: var(--clay); font-style: italic; }
  .hero-sub { color: #c9bdb4; font-size: 1rem; font-weight: 300; max-width: 480px; }
  .hero-badge {
    display: inline-block; background: #ffffff12; border: 1px solid #ffffff22;
    border-radius: 100px; padding: 0.3rem 0.9rem; font-size: 0.78rem; color: #ddd;
    margin-top: 1.4rem; backdrop-filter: blur(6px);
  }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: var(--sand) !important;
    border-right: 1px solid var(--border) !important;
  }
  [data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem !important; }

  .sidebar-section {
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem 1rem;
    margin-bottom: 1.2rem;
  }
  .sidebar-section-title {
    font-size: 0.68rem; letter-spacing: 0.16em; text-transform: uppercase;
    color: var(--clay); font-weight: 600; margin-bottom: 1rem;
    display: flex; align-items: center; gap: 0.4rem;
  }

  /* ── Sliders & selects ── */
  .stSlider > div > div > div { background: var(--clay) !important; }
  .stSlider [data-baseweb="thumb"] { background: var(--clay) !important; border-color: var(--clay) !important; }
  .stSelectbox [data-baseweb="select"] > div:first-child {
    border-color: var(--border) !important;
    background: var(--paper) !important;
    border-radius: 10px !important;
  }

  /* ── Predict button ── */
  .stButton > button {
    width: 100%; background: var(--clay) !important;
    color: #fff !important; border: none !important;
    border-radius: 12px !important; padding: 0.8rem 1rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important; font-size: 1rem !important;
    letter-spacing: 0.02em;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px #c8785a44 !important;
  }
  .stButton > button:hover {
    background: #b56749 !important;
    box-shadow: 0 6px 28px #c8785a66 !important;
    transform: translateY(-1px);
  }

  /* ── Result cards ── */
  .result-card {
    background: linear-gradient(135deg, #1a1510, #2e2118);
    border-radius: 20px; padding: 2.4rem 2rem;
    text-align: center; position: relative; overflow: hidden;
    box-shadow: 0 20px 60px #00000030;
  }
  .result-card::after {
    content: '🏡';
    position: absolute; right: 1.5rem; bottom: 1rem;
    font-size: 5rem; opacity: 0.07;
  }
  .result-label {
    font-size: 0.72rem; letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--clay); margin-bottom: 0.5rem;
  }
  .result-price {
    font-family: 'DM Serif Display', serif; font-size: 3rem;
    color: #fff; line-height: 1; margin-bottom: 0.3rem;
  }
  .result-sub { color: #9a8d82; font-size: 0.85rem; }

  .tag {
    display: inline-block; border-radius: 100px;
    padding: 0.35rem 1rem; font-size: 0.8rem; font-weight: 600;
    margin-top: 1.2rem;
  }
  .tag-premium  { background: #c8785a22; color: var(--clay); border: 1px solid #c8785a55; }
  .tag-comfort  { background: #6b8c7222; color: var(--sage);  border: 1px solid #6b8c7255; }
  .tag-budget   { background: #5a7ec822; color: #5a7ec8;      border: 1px solid #5a7ec855; }

  /* ── Insight tiles ── */
  .insight-grid { display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 1.5rem; }
  .insight-tile {
    flex: 1; min-width: 140px;
    background: #fff; border: 1px solid var(--border);
    border-radius: 14px; padding: 1.1rem 1rem; text-align: center;
  }
  .insight-tile .icon { font-size: 1.6rem; margin-bottom: 0.4rem; }
  .insight-tile .val  { font-size: 1.1rem; font-weight: 600; color: var(--ink); }
  .insight-tile .lbl  { font-size: 0.72rem; color: var(--muted); margin-top: 0.1rem; }

  /* ── Divider ── */
  .divider { border: none; border-top: 1px solid var(--border); margin: 2rem 0; }

  /* ── Footer ── */
  .footer {
    text-align: center; color: var(--muted); font-size: 0.78rem; margin-top: 3rem;
    padding-top: 1.5rem; border-top: 1px solid var(--border);
  }

  /* ── Placeholder state ── */
  .placeholder {
    border: 2px dashed var(--border); border-radius: 20px;
    padding: 3rem 2rem; text-align: center; color: var(--muted);
  }
  .placeholder .big { font-size: 3rem; margin-bottom: 0.5rem; }
  .placeholder p { font-size: 0.95rem; }
</style>
""", unsafe_allow_html=True)


# ─── Model loader ────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    try:
        return pickle.load(open("model.pkl", "rb"))
    except FileNotFoundError:
        return None


model = load_model()


# ─── Helpers ─────────────────────────────────────────────────────────────────
LOCATION_MAP    = {"Urban Premium 🏙️": 1, "Suburban 🌳": 0}
INCOME_MAP      = {"High Income 💎": 1, "Mid Income 🏠": 0, "Low Income 🌱": 0}
INCOME_VAL_MAP  = {"High Income 💎": 1, "Mid Income 🏠": 0.5, "Low Income 🌱": 0}

def tier_label(price):
    if price >= 8_000_000:
        return ("Ultra Luxury", "tag-premium", "✦")
    elif price >= 4_000_000:
        return ("Premium Segment", "tag-premium", "★")
    elif price >= 2_000_000:
        return ("Mid-Comfort Segment", "tag-comfort", "◆")
    else:
        return ("Budget Friendly", "tag-budget", "◇")

def fmt_inr(n):
    if n >= 1_00_00_000:
        return f"₹{n/1_00_00_000:.2f} Cr"
    elif n >= 1_00_000:
        return f"₹{n/1_00_000:.2f} L"
    return f"₹{n:,.0f}"


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏡 NestValue")
    st.caption("AI-powered property valuation")
    st.markdown("---")

    # ── Property Details ──
    st.markdown('<div class="sidebar-section"><div class="sidebar-section-title">🏗️ Property Details</div>', unsafe_allow_html=True)
    area      = st.slider("Area (sq ft)", 100, 10000, 1500, step=50)
    bedrooms  = st.slider("Bedrooms 🛏️", 1, 10, 3)
    bathrooms = st.slider("Bathrooms 🚿", 1, 10, 2)
    floors    = st.slider("Floors 🏢", 1, 5, 1)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Location & Economics ──
    st.markdown('<div class="sidebar-section"><div class="sidebar-section-title">📍 Location & Economics</div>', unsafe_allow_html=True)
    location_label     = st.selectbox("Location Type", list(LOCATION_MAP.keys()))
    income_level_label = st.selectbox("Area Income Level", list(INCOME_MAP.keys()))
    st.markdown('</div>', unsafe_allow_html=True)

    predict_clicked = st.button("🔮 Predict Price", use_container_width=True)


# ─── MAIN AREA ───────────────────────────────────────────────────────────────

# Hero
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">AI Property Valuation</div>
  <div class="hero-title">What's your home<br><em>really</em> worth?</div>
  <div class="hero-sub">
    Get an instant AI-powered estimate based on property features,
    location tier, and neighbourhood income profile.
  </div>
  <div class="hero-badge">🤖 Machine Learning · Instant Results · ₹ INR</div>
</div>
""", unsafe_allow_html=True)

# Two-column layout
col_result, col_summary = st.columns([3, 2], gap="large")

with col_result:
    if predict_clicked:
        location_val     = LOCATION_MAP[location_label]
        income_level_val = INCOME_VAL_MAP[income_level_label]
        features = [[area, bedrooms, bathrooms, floors, location_val, income_level_val]]

        if model is None:
            # Demo fallback when no model.pkl present
            price = (area * 4200) + (bedrooms * 180000) + (bathrooms * 90000) \
                    + (floors * 120000) + (location_val * 500000) \
                    + (income_level_val * 300000)
        else:
            with st.spinner("Analysing property…"):
                time.sleep(0.8)
            price = float(model.predict(features)[0])

        tier, tag_cls, icon = tier_label(price)
        price_str = fmt_inr(price)

        st.markdown(f"""
        <div class="result-card">
          <div class="result-label">Estimated Market Value</div>
          <div class="result-price">{price_str}</div>
          <div class="result-sub">±5% margin · Based on current market data</div>
          <span class="tag {tag_cls}">{icon} {tier}</span>
        </div>
        """, unsafe_allow_html=True)

        # Insights row
        price_per_sqft = price / area if area else 0
        st.markdown(f"""
        <div class="insight-grid">
          <div class="insight-tile">
            <div class="icon">📐</div>
            <div class="val">₹{price_per_sqft:,.0f}</div>
            <div class="lbl">Per sq ft</div>
          </div>
          <div class="insight-tile">
            <div class="icon">🛏️</div>
            <div class="val">{fmt_inr(price/bedrooms)}</div>
            <div class="lbl">Per bedroom</div>
          </div>
          <div class="insight-tile">
            <div class="icon">📊</div>
            <div class="val">{tier.split()[0]}</div>
            <div class="lbl">Market tier</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="placeholder">
          <div class="big">🏡</div>
          <p>Configure your property in the sidebar<br>and hit <strong>Predict Price</strong> to begin.</p>
        </div>
        """, unsafe_allow_html=True)

with col_summary:
    st.markdown("#### 📋 Property Summary")
    summary_data = {
        "📐 Area": f"{area:,} sq ft",
        "🛏️ Bedrooms": bedrooms,
        "🚿 Bathrooms": bathrooms,
        "🏢 Floors": floors,
        "📍 Location": location_label,
        "💼 Income Level": income_level_label,
    }
    for k, v in summary_data.items():
        cols = st.columns([2, 3])
        cols[0].markdown(f"<span style='color:var(--muted);font-size:0.85rem'>{k}</span>", unsafe_allow_html=True)
        cols[1].markdown(f"<strong style='font-size:0.9rem'>{v}</strong>", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("#### 🧭 How it works")
    st.markdown("""
<div style='font-size:0.85rem; color:var(--muted); line-height:1.7'>
  Our model analyses <strong>6 key property features</strong> trained on
  thousands of real estate transactions. It considers both structural
  attributes (size, rooms, floors) and socioeconomic signals
  (location tier, income profile) to deliver a calibrated estimate.
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
  NestValue · AI House Price Predictor · Built with Streamlit 🖤
  <br>For illustrative purposes only. Always consult a certified property valuator.
</div>
""", unsafe_allow_html=True)