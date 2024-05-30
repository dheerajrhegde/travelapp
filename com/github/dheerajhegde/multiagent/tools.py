from typing import Any

from crewai_tools import BaseTool
import com.github.dheerajhegde.googlesearch.GoogleSearch as gs

class PointsOfInterest(BaseTool):
    name: str = "Find specific points of interest in a city"
    description: str = ("This tool helps you find specific points of interest in a city."
                        "Given the city and activities that you are interested in.")
    """def __init__(self):
        self.args_dict = None

    def set_args(self, args_dict):
        self.args_dict = args_dict"""

    def _run(self, city, activities):
        """city = self.args_dict.get("city")
        activities = self.args_dict.get("activities")
        api_key = self.args_dict.get("api_key")"""
        return gs.find_place(city, activities)

class InformationOnPointOfInterest(BaseTool):
    name: str = "Get information on a point of interest"
    description: str = ("This tool helps you get information on a point of interest."
                        "Given the place ID of the point of interest.")
    """def __init__(self):
        self.args_dict = {}
    def set_args(self, args_dict):
        self.args_dict = args_dict"""

    def _run(self, place_id: str):
        return gs.get_place_operating_hours(place_id)

class BusyTimes(BaseTool):
    name: str = "Find how busy a place is"
    description: str = ("This tool helps you find how busy a place is "
                        "at any given hour of the day. Given the name and address of the place.")
    """def __init__(self):
        self.args_dict = {}
    def set_args(self, args_dict):
        self.args_dict = args_dict"""

    def _run(self, name: str, address: str):
        return gs.get_populartimes_from_search(name, address)

class Food(BaseTool):
    name: str = "Get information where to eat"
    description: str = ("This tool helps you get information the best places to eat "
                        "Given the given the food preference and the city.")
    """def __init__(self):
        self.args_dict = {}
    def set_args(self, args_dict):
        self.args_dict = args_dict"""

    def _run(self, city, food_preference):
        return gs.find_place(city, food_preference)