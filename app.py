import streamlit as st
import pickle

# Load model
model = pickle.load(open("model.pkl", "rb"))

st.set_page_config(page_title="House Price Predictor", layout="centered")

# Title
st.title("House Price Prediction App")
st.write("Enter details to predict house price")

# Inputs
area = st.number_input("Area (sq ft)", min_value=100, max_value=10000, value=1000)
bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, value=3)
bathrooms = st.number_input("Bathrooms", min_value=1, max_value=10, value=2)
floors = st.number_input("Floors", min_value=1, max_value=5, value=1)
location = st.number_input("Location", min_value=0, max_value=1, value=1)
income_level = st.number_input("Income Level", min_value=0, max_value=1, value=1)

# Predict button
if st.button("Predict Price"):
    features = [[area, bedrooms, bathrooms, floors, location, income_level]]
    prediction = model.predict(features)
    
    st.success(f"💰 Estimated Price: ₹ {prediction[0]:,.2f}")