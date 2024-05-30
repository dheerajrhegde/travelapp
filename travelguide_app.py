import streamlit as st
import datetime
from com.github.dheerajhegde.multiagent.travelplanner import TravelPlanner

st.title("Get your travel guide here!")
city = st.text_input("City", "New York City")
arrival_date = st.date_input("Date of arrival", datetime.date(2024, 5, 30))
arrival_time = st.time_input("Time of arrival",datetime.time(6, 0, 0))
departure_date = st.date_input("Date of departure", datetime.date(2024, 5, 31))
departure_time = st.time_input("Time of departure", datetime.time(23, 0, 0))

activities = st.multiselect("What would you like to do?", ["Museum", "Shopping", "Parks", "Relaxing", "Landmarks"], default=["Museum"])
preference = st.radio("Food Preference?", ["Indian", "Chinese", "Italian", "Mexican", "American"])

args_dict = {
    "city": city,
    "arrival_date": arrival_date,
    "arrival_time": arrival_time,
    "departure_date": departure_date,
    "departure_time": departure_time,
    "activities": activities,
    "food_preference": preference
}

tp = TravelPlanner(args_dict)
output = tp.plan()
st.write(output)