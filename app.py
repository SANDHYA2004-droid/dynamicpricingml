import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

# Page config
st.set_page_config(page_title="Dynamic Pricing System", layout="centered")

# Load trained model
model = joblib.load("pricing_model.pkl")

# Business Logic Function
def dynamic_price(demand, competitor_price, time):
    base_price = model.predict([[demand, competitor_price, time]])[0]
    
    if demand > 80:
        base_price += 15
    elif demand < 30:
        base_price -= 15
        
    if time == 1:
        base_price += 10
        
    if competitor_price < base_price:
        base_price -= 5
        
    return round(base_price, 2)

# Explanation Function
def explain_price(demand, competitor_price, time, predicted_price):
    reasons = []
    
    if demand > 80:
        reasons.append("High demand → price increased")
    elif demand < 30:
        reasons.append("Low demand → discount applied")
    else:
        reasons.append("Moderate demand → stable pricing")
        
    if time == 1:
        reasons.append("Peak time → price increased")
    else:
        reasons.append("Normal time → standard pricing")
        
    if competitor_price < predicted_price:
        reasons.append("Competitor price is lower → adjusted price to stay competitive")
    else:
        reasons.append("Competitor price is higher → price optimized for profit")
        
    return reasons

# UI
st.title("💰 Dynamic Pricing System")
st.markdown("### Smart ML-based price optimization")

st.write("Adjust inputs to predict optimal price")

# Inputs
demand = st.slider("Demand", 0, 100, 50)
competitor_price = st.slider("Competitor Price", 50, 200, 100)
time = st.selectbox("Time", ["Normal", "Peak"])

time_val = 1 if time == "Peak" else 0

# Prediction
if st.button("Predict Price"):
    price = dynamic_price(demand, competitor_price, time_val)
    
    st.success(f"💰 Suggested Price: ₹{price}")
    
    # Explanation
    st.subheader("🧠 Explanation")
    reasons = explain_price(demand, competitor_price, time_val, price)
    
    for r in reasons:
        st.write("•", r)
    
    # Graph
    st.subheader("📊 Demand vs Predicted Price")
    
    sample_demand = list(range(10, 101, 10))
    predicted_prices = [
        dynamic_price(d, competitor_price, time_val) for d in sample_demand
    ]
    
    plt.figure()
    plt.plot(sample_demand, predicted_prices)
    plt.xlabel("Demand")
    plt.ylabel("Price")
    plt.title("Demand vs Predicted Price")
    
    st.pyplot(plt)
