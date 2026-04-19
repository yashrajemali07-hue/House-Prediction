import streamlit as st
import pickle
import time

# ─── Sidebar State Fix ─────────────────────────
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

# ─── Page Config ───────────────────────────────
st.set_page_config(
    page_title="NestValue · House Price AI",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state=st.session_state.sidebar_state,
)

# ─── Custom CSS (UPDATED) ──────────────────────
st.markdown("""
<style>

/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Colors ── */
:root {
  --clay:#c8785a;
  --clay-dim:#9e5c42;
  --ink:#1a1510;
  --paper:#fdf8f3;
  --border:#e2d5c8;
  --muted:#8a7b6e;
  --sage:#6b8c72;

  --sb-bg:#1a1510;
  --sb-surface:#24201a;
  --sb-border:#38302a;
  --sb-text:#e8ddd4;
}

/* ── Base ── */
html, body {
  font-family:'DM Sans', sans-serif;
  background-color: var(--paper);
  color: var(--ink);
}

/* ── iOS Sliding Sidebar ── */
[data-testid="stSidebar"] {
  transform: translateX(0);
  transition: transform 0.35s cubic-bezier(0.25,0.8,0.25,1);
  will-change: transform;
  box-shadow: 4px 0 24px rgba(0,0,0,0.25);
}

section[data-testid="stSidebar"][aria-expanded="false"] {
  transform: translateX(-100%);
}

/* DO NOT override display/visibility */

/* ── Hero ── */
.hero {
  background: linear-gradient(135deg,#1a1510,#2e2118);
  border-radius:18px;
  padding:3rem;
  margin-bottom:2rem;
  color:white;
}

/* ── Button ── */
.stButton>button {
  background:var(--clay);
  color:white;
  border:none;
  border-radius:10px;
  padding:10px;
  font-weight:600;
}

/* ── Result ── */
.result-card {
  background:#1a1510;
  color:white;
  padding:2rem;
  border-radius:16px;
  text-align:center;
  box-shadow:0 10px 30px rgba(0,0,0,0.2);
}

</style>
""", unsafe_allow_html=True)

# ─── Load Model ────────────────────────────────
@st.cache_resource
def load_model():
    try:
        return pickle.load(open("model.pkl", "rb"))
    except:
        return None

model = load_model()

# ─── Sidebar ──────────────────────────────────
with st.sidebar:
    st.title("NestValue")

    area = st.number_input("Area", 100, 10000, 1500)
    bedrooms = st.number_input("Bedrooms", 1, 10, 3)
    bathrooms = st.number_input("Bathrooms", 1, 10, 2)
    floors = st.number_input("Floors", 1, 5, 1)

    location = st.selectbox("Location", ["Low","Medium","Premium"])
    income = st.selectbox("Income", ["Low","Medium","High"])

    predict = st.button("Predict Price")

# ─── Reopen Button (Failsafe) ──────────────────
if st.button("☰ Open Controls"):
    st.session_state.sidebar_state = "expanded"
    st.rerun()

# ─── Main UI ───────────────────────────────────
st.markdown("""
<div class="hero">
<h1>What's your home really worth?</h1>
<p>AI-powered price prediction</p>
</div>
""", unsafe_allow_html=True)

# ─── Prediction ────────────────────────────────
if predict:

    loc_map = {"Low":0, "Medium":1, "Premium":2}
    inc_map = {"Low":0, "Medium":1, "High":2}

    features = [[area, bedrooms, bathrooms, floors,
                 loc_map[location], inc_map[income]]]

    if model:
        price = model.predict(features)[0]
    else:
        price = (
            area*4000 +
            bedrooms*200000 +
            bathrooms*100000 +
            floors*120000 +
            loc_map[location]*500000 +
            inc_map[income]*300000
        )

    with st.spinner("Predicting..."):
        time.sleep(0.5)

    st.markdown(f"""
    <div class="result-card">
        <h2>₹{price:,.0f}</h2>
        <p>Estimated Price</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.info("Enter details in sidebar and click Predict")
