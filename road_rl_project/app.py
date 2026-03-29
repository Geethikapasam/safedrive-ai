import streamlit as st
import requests
from model import get_best_action, get_risk_score


API_KEY = "1c073c113c53c9d63cc6a8ad068415b1"

st.title(" SafeDrive AI")
st.subheader("AI-Based Driving Safety Monitor 🚦")

#  Inputs
speed = st.slider("Speed", 0, 180, 60)
time = st.selectbox("Time", ["day", "night"])

#  Location input
city = st.text_input("Enter City", "Visakhapatnam")

#  WEATHER CODE
weather = "clear"

try:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url).json()

    if response.get("cod") != 200:
        st.error("❌ City not found. Please enter correct name.")
    else:
        weather_main = response["weather"][0]["main"].lower()

        # ✅ Weather classification
        if weather_main in ["rain", "drizzle", "thunderstorm"]:
            weather = "rain"
            st.warning(f" Weather in {city}: {weather_main}")

        elif weather_main in ["mist", "fog", "haze", "smoke"]:
            weather = "rain"  # treat as risky
            st.warning(f" Weather in {city}: {weather_main} (Low visibility!)")

        else:
            weather = "clear"
            st.success(f" Weather in {city}: {weather_main}")

except Exception as e:
    st.error(f" API Error: {e}")

#  Accident zone logic
zone = "normal"
if "highway" in city.lower() or "ghat" in city.lower():
    zone = "accident_prone"

#  Button action
if st.button("Check Risk"):
    #  Rounding
    speed_rounded = round(speed / 10) * 10

    state = (speed_rounded, weather, time)
    action = get_best_action(state)

    # Risk
    risk = get_risk_score(speed, weather, time, zone)

    #  Output
    st.write("###  Recommended Action:", action)
    st.write(f"### Risk Level: {risk}%")

    # Progress bar
    st.progress(risk / 100)

    # Graph
    st.line_chart({"Risk": [risk]})

    #  Zone alert
    if zone == "accident_prone":
        st.error(" Accident-prone zone detected!")

    #  Final message
    if risk > 70:
        st.error(" High Risk! Slow down")
    elif risk > 40:
        st.warning(" Moderate Risk")
    else:
        st.success("✅ Safe")