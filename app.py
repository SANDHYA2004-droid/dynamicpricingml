import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Load dataset
df = pd.read_csv("dynamic_pricing.csv")

# Train model
X = df[['Demand', 'Competitor_Price', 'Time']]
y = df['Price']

model = RandomForestRegressor()
model.fit(X, y)

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
def explain_price(demand, competitor_price, time):
    reasons = []
    
    if demand > 80:
        reasons.append("High demand → price increased")
    elif demand < 30:
        reasons.append("Low demand → discount applied")
        
    if time == 1:
        reasons.append("Peak time → price increased")
        
    if competitor_price < 100:
        reasons.append("Competitor price low → adjusted price")
        
    return reasons

# UI
st.title("💰 Dynamic Pricing System")

st.write("Enter values to predict optimal price")

# Inputs
demand = st.slider("Demand", 0, 100, 50)
competitor_price = st.slider("Competitor Price", 50, 200, 100)
time = st.selectbox("Time", ["Normal", "Peak"])

time_val = 1 if time == "Peak" else 0

# Button
if st.button("Predict Price"):
    price = dynamic_price(demand, competitor_price, time_val)
    
    st.success(f"💰 Suggested Price: ₹{price}")
    
    st.subheader("Explanation:")
    reasons = explain_price(demand, competitor_price, time_val)
    
    for r in reasons:
        st.write("•", r)