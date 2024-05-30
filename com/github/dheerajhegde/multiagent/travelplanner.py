from crewai import Agent, Task, Crew
import os, json
import requests
import com.github.dheerajhegde.googlesearch.GoogleSearch as gs
import com.github.dheerajhegde.multiagent.tools as tools

class TravelPlanner():
    def __init__(self, args_dict):
        os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'
        self.city = args_dict.get("city")
        self.arrival_date = args_dict.get("arrival_date")
        self.arrival_time = args_dict.get("arrival_time")
        self.departure_date = args_dict.get("departure_date")
        self.departure_time = args_dict.get("departure_time")
        self.activities = args_dict.get("activities")
        self.foodPreference = args_dict.get("food_preference")

        #self.api_key="AIzaSyDRXbm3xf9lH2Y5A7Sv97DeRhzk0-8PoRk"
        self.points_of_interest = tools.PointsOfInterest()
        #self.points_of_interest.set_args(args_dict)
        self.information_on_point_of_interest = tools.InformationOnPointOfInterest()
        #self.information_on_point_of_interest.set_args(args_dict)
        self.busy_times = tools.BusyTimes()
        #self.busy_times.set_args(args_dict)
        self.food = tools.Food()
        #self.food.set_args(args_dict)

    def plan(self):
        # create agent
        local_guide = Agent(
            role="Expert local guide who knows which places to visit and when.",
            goal="Based on the schedule provided, list out best points of interest to visit, "
                 "their busy times, average time spent, based on the schedule provided.",
            tools=[self.points_of_interest, self.information_on_point_of_interest, self.busy_times, self.food],
            backstory=(
                "As an expert local guide who has lived in the city of many years, "
                "you know the places to visit based on the schedule and activities provided. "
                "You list out the best places to visit based on preferences, their busy times, "
                "average time spent in the place, and the location of the places to visit."
            )
        )
        where_to_go = Task(
            description=(
                "You are given a set of parameters in as follows: "
                "city visiting - {city} "
                "arrival date - {arrival_date} "
                "arrival time - {arrival_time} "
                "departure date - {departure_date} "
                "departure time - {departure_time} "
                "activities the person is interested in - {activities} "
                "lunch preference - {foodPreference} "
                "dinner preference - {foodPreference} "
                "Based on information above, please list out the best places to visit, "
                "in the city, average time to spend in each place, and the busy times. "
                "You will have to work with the food critic to find places to eat at "
                "such that the person can visit all the places and eat at the best places."
            ),
            expected_output=(
                "List of places to visit, average time spent in each place, and the busy times."
            ),
            agent=local_guide,
            async_execution=False,
            allow_delegation=True
        )
        foodie = Agent(
            role="An expert food critic who can help you find the best places to eat.",
            goal="Find the best place to eat based on the food preference provided.",
            tools=[self.points_of_interest, self.information_on_point_of_interest, self.busy_times, self.food],
            backstory=(
                "As an expert food critic, you know the best places to eat in the city. "
                "You can help find the best place to eat based on the food preference provided "
                "and the schedule of activities and the location of the places to visit."
            )
        )
        where_to_eat = Task(
            description=(
                "You are given a set of parameters in as follows: "
                "city visiting - {city} "
                "arrival date - {arrival_date} "
                "arrival time - {arrival_time} "
                "departure date - {departure_date} "
                "departure time - {departure_time} "
                "activities the person is interested in - {activities} "
                "lunch preference - {foodPreference} "
                "dinner preference - {foodPreference} "
                "You will be proivided with a list of places the person will be visiting. "
                "You need to work with the local guide and planned who will be deciding the places "
                "to visit and scheduled for the visit."
            ),
            expected_output=(
                "One place to eat at for lunch and one place to eat at for dinner. "
                "These recommended places should play well with the schedule and places to visit."
            ),
            agent=foodie,
            async_execution=False,
            allow_delegation=True
        )
        planner = Agent(
            role="Expert travel planner who can help you create itinerary for your trip.",
            goal="Put together the best itinerary based on the schedule, places to visit, and places to eat at.",
            tools=[self.points_of_interest, self.information_on_point_of_interest, self.busy_times, self.food],
            backstory=(
                "As an expert travel planner, you use the information provided by the local travel guide, "
                "the food critic, and the schedule to put together the best itinerary for the trip. "
                "You take into account the day and time the person will be in the city and "
                "put together an iterinary to make the most of the trip."
            )
        )
        plan_trip = Task(
            description=(
                "You are given a set of parameters in as follows: "
                "city visiting - {city} "
                "arrival date - {arrival_date} "
                "arrival time - {arrival_time} "
                "departure date - {departure_date} "
                "departure time - {departure_time} "
                "activities the person is interested in - {activities} "
                "lunch preference - {foodPreference} "
                "dinner preference - {foodPreference} "
                "Local guide will also provide you with the places to visit with information "
                "about the places to visit the average time of visit and the busy times. "
                "You will also know the recommended places to eat lunch and dinner. "
                "Based on this information, you need to put together the best itinerary for the trip."
                "The itinerary should be sequential with clear recomemndation on the first, second, third, etc. "
                "places to visit and should take into account the open and close times "
                "of the identified places of interest. Make sure the itirinery is practical and a person can visit "
                "it based on the time he/she is in the city. "
            ),
            expected_output=(
                "A detailed itinerary for the trip with "
                "- the places to visit "
                "- the average time to in each place, "
                "- Time to get to that place "
                "- Name and address of the place. "
                "Provide the data in simple JSON output format"
            ),
            agent=planner,
            async_execution=False,
            allow_delegation=True
        )
        parameters = {
            "city": self.city,
            "arrival_date": self.arrival_date,
            "arrival_time": self.arrival_time,
            "departure_date": self.departure_date,
            "departure_time": self.departure_time,
            "activities": self.activities,
            "foodPreference": self.foodPreference
        }
        planing_crew = Crew(
            agents=[local_guide, foodie, planner],
            tasks=[where_to_go, where_to_eat, plan_trip],
            verbose=True
        )

        result = planing_crew.kickoff(parameters)
        return result