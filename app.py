import streamlit as st
import pickle
import time

# ─── Page Config ─────────────────────────────────────────
st.set_page_config(
    page_title="NestValue · Premium AI",
    page_icon="🏡",
    layout="wide"
)

# ─── Load Model ──────────────────────────────────────────
@st.cache_resource
def load_model():
    try:
        return pickle.load(open("model.pkl", "rb"))
    except:
        return None

model = load_model()

# ─── Styling (Glass UI) ──────────────────────────────────
st.markdown("""
<style>
body {
    background: linear-gradient(135deg,#0f0c29,#302b63,#24243e);
    color: white;
}

.main {
    background: transparent;
}

.glass {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(14px);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.15);
}

.title {
    font-size: 3rem;
    font-weight: bold;
}

.sub {
    color: #ccc;
    margin-bottom: 20px;
}

.stButton>button {
    background: linear-gradient(135deg,#ff9966,#ff5e62);
    border: none;
    border-radius: 10px;
    padding: 12px;
    color: white;
    font-weight: bold;
}

.result {
    font-size: 2.5rem;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ─── Title ───────────────────────────────────────────────
st.markdown("""
<div class='title'>NestValue AI</div>
<div class='sub'>Modern house price prediction</div>
""", unsafe_allow_html=True)

# ─── Layout ──────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)

    area = st.number_input("Area (sq ft)", 100, 10000, 1500)
    bedrooms = st.number_input("Bedrooms", 1, 10, 3)
    bathrooms = st.number_input("Bathrooms", 1, 10, 2)
    floors = st.number_input("Floors", 1, 5, 1)

    location = st.selectbox("Location", ["Low","Medium","Premium"])
    income = st.selectbox("Income Level", ["Low","Medium","High"])

    predict = st.button("Predict Price")

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)

    if predict:
        loc_map = {"Low":0, "Medium":0.5, "Premium":1}
        inc_map = {"Low":0, "Medium":0.5, "High":1}

        features = [[area, bedrooms, bathrooms, floors,
                     loc_map[location], inc_map[income]]]

        if model:
            price = model.predict(features)[0]
        else:
            price = (
                area*4000 + bedrooms*200000 + bathrooms*100000 +
                floors*120000 + loc_map[location]*500000 + inc_map[income]*300000
            )

        time.sleep(0.5)

        st.markdown(f"""
        <div class='result'>₹{price:,.0f}</div>
        <div>Estimated Price</div>
        """, unsafe_allow_html=True)

    else:
        st.write("Enter details to predict price")

    st.markdown("</div>", unsafe_allow_html=True)
