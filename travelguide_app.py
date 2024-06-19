# Description: A Streamlit web app that allows users to input their travel preferences
# and generates a personalized travel plan.

# Importing the required libraries
import streamlit as st  # Streamlit for creating a web app
import datetime  # Datetime for handling date and time inputs
from com.github.dheerajhegde.multiagent.travelplanner import TravelPlanner  # Custom travel planner module

# Setting the title of the Streamlit app
st.title("Get your travel guide here!")

# Input field for the user to enter the city name, defaulting to "New York City"
city = st.text_input("City", "New York City")

# Input field for the user to select the arrival date, defaulting to May 30, 2024
arrival_date = st.date_input("Date of arrival", datetime.date(2024, 5, 30))

# Input field for the user to select the arrival time, defaulting to 6:00 AM
arrival_time = st.time_input("Time of arrival", datetime.time(6, 0, 0))

# Input field for the user to select the departure date, defaulting to May 31, 2024
departure_date = st.date_input("Date of departure", datetime.date(2024, 5, 31))

# Input field for the user to select the departure time, defaulting to 11:00 PM
departure_time = st.time_input("Time of departure", datetime.time(23, 0, 0))

# Multi-select field for the user to choose activities they are interested in, defaulting to "Museum"
activities = st.multiselect(
    "What would you like to do?",  # Label for the multi-select input
    ["Museum", "Shopping", "Parks", "Relaxing", "Landmarks"],  # Options available for selection
    default=["Museum"]  # Default selection
)

# Radio button field for the user to choose their food preference
preference = st.radio(
    "Food Preference?",  # Label for the radio button input
    ["Indian", "Chinese", "Italian", "Mexican", "American"]  # Options available for selection
)

# Creating a dictionary with all user inputs to be passed to the TravelPlanner
args_dict = {
    "city": city,  # User-inputted city
    "arrival_date": arrival_date,  # User-selected arrival date
    "arrival_time": arrival_time,  # User-selected arrival time
    "departure_date": departure_date,  # User-selected departure date
    "departure_time": departure_time,  # User-selected departure time
    "activities": activities,  # User-selected activities
    "foodPreference": preference  # User-selected food preference
}

# Initializing the TravelPlanner with the user inputs
tp = TravelPlanner(args_dict)

# Generating the travel plan based on the inputs
output = tp.plan()

# Displaying the generated travel plan in the Streamlit app
st.write(output)