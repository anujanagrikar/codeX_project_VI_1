# app.py

import streamlit as st
from main import predict_price

st.set_page_config(page_title="CodeX Beverage Price Prediction", layout="wide")

st.title("CodeX Beverage: Price Prediction")

# -----------------------------
# Row 1
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    age = st.number_input("Age", min_value=18, max_value=70, value=28)

with col2:
    gender = st.selectbox("Gender", ['M', 'F'])

with col3:
    zone = st.selectbox(
        "Zone",
        ['Urban', 'Metro', 'Semi-Urban', 'Rural']
    )

with col4:
    occupation = st.selectbox(
        "Occupation",
        ['Student', 'Working Professional', 'Entrepreneur', 'Retired']
    )

# -----------------------------
# Row 2
# -----------------------------
col5, col6, col7, col8 = st.columns(4)

with col5:
    income_levels = st.selectbox(
        "Income Level (In L)",
        ['<10L', '10L- 15L', '16L- 25L', '26L- 35L', '>35L', 'Not Reported']
    )

with col6:
    consume_frequency = st.selectbox(
        "Consume Frequency (weekly)",
        ['0-2 times', '3-4 times', '5-7 times']
    )

with col7:
    current_brand = st.selectbox(
        "Current Brand",
        ['Established', 'Newcomer']
    )

with col8:
    preferable_consumption_size = st.selectbox(
        "Preferable Consumption Size",
        ['Small (250 ml)', 'Medium (500 ml)', 'Large (1 L)']
    )

# -----------------------------
# Row 3
# -----------------------------
col9, col10, col11, col12 = st.columns(4)

with col9:
    awareness_of_other_brands = st.selectbox(
        "Awareness of other brands",
        ['0to1', '2to4', 'above 4']
    )

with col10:
    reasons_for_choosing_brands = st.selectbox(
        "Reasons for choosing brands",
        ['Price', 'Quality', 'Taste', 'Availability', 'Brand Reputation']
    )

with col11:
    flavor_preference = st.selectbox(
        "Flavor Preference",
        ['Traditional', 'Exotic', 'Mixed']
    )

with col12:
    purchase_channel = st.selectbox(
        "Purchase Channel",
        ['Online', 'Retail Store']
    )

# -----------------------------
# Row 4
# -----------------------------
col13, col14, col15 = st.columns(3)

with col13:
    packaging_preference = st.selectbox(
        "Packaging Preference",
        ['Simple', 'Premium', 'Eco-Friendly']
    )

with col14:
    health_concerns = st.selectbox(
        "Health Concerns",
        ['Low (Not very concerned)', 'Moderate', 'High']
    )

with col15:
    typical_consumption_situations = st.selectbox(
        "Typical Consumption Situations",
        ['Active (eg. Sports, gym)', 'Casual', 'Parties', 'Work/Study']
    )

# -----------------------------
# Prediction Button
# -----------------------------
if st.button("Calculate Price Range"):

    user_data = {
        'age': age,
        'gender': gender,
        'zone': zone,
        'occupation': occupation,
        'income_levels': income_levels,
        'consume_frequency(weekly)': consume_frequency,
        'current_brand': current_brand,
        'preferable_consumption_size': preferable_consumption_size,
        'awareness_of_other_brands': awareness_of_other_brands,
        'reasons_for_choosing_brands': reasons_for_choosing_brands,
        'flavor_preference': flavor_preference,
        'purchase_channel': purchase_channel,
        'packaging_preference': packaging_preference,
        'health_concerns': health_concerns,
        'typical_consumption_situations': typical_consumption_situations
    }

    prediction = predict_price(user_data)

    st.success(f"Predicted Price Range: {prediction}")

