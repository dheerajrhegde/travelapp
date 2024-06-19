from typing import Any

from crewai_tools import BaseTool
import com.github.dheerajhegde.googlesearch.GoogleSearch as gs

class PointsOfInterest(BaseTool):
    """
    PointsOfInterest is a tool for finding specific points of interest (POIs) in a city based on given activities.

    Attributes:
        name (str): The name of the tool.
        description (str): A brief description of what the tool does.
    """

    name: str = "Find specific points of interest in a city"
    description: str = ("This tool helps you find specific points of interest in a city."
                        "Given the city and activities that you are interested in.")

    def _run(self, city, activities):
        """
        Runs the tool to find points of interest based on the provided city and activities.

        This method retrieves the 'city' and 'activities' from the instance's args_dict,
        then uses an external service to find relevant places.

        Args:
            city (str): The name of the city to search for points of interest.
            activities (list[str]): A list of activities to find related points of interest.

        Returns:
            list[dict]: A list of points of interest that match the given criteria.
        """
        return gs.find_place(city, activities)

class InformationOnPointOfInterest(BaseTool):
    """
    InformationOnPointOfInterest is a tool designed to retrieve detailed information about a specific point of interest (POI).

    Attributes:
        name (str): The name of the tool.
        description (str): A brief description of what the tool does.
    """
    name: str = "Get information on a point of interest"
    description: str = ("This tool helps you get information on a point of interest."
                        "Given the place ID of the point of interest.")

    def _run(self, place_id: str):
        """
        Executes the tool to get information on a point of interest using its place ID.

        This method interacts with an external service to fetch operating hours or other relevant details
        for the specified point of interest.

        Args:
            place_id (str): The unique identifier for the point of interest.

        Returns:
            dict: A dictionary containing information about the operating hours of the place.
        """
        return gs.get_place_operating_hours(place_id)

class BusyTimes(BaseTool):
    """
    BusyTimes is a tool for finding out how busy a place is at different times of the day.

    Attributes:
        name (str): The name of the tool.
        description (str): A brief description of the tool's functionality.
    """
    name: str = "Find how busy a place is"
    description: str = ("This tool helps you find how busy a place is "
                        "at any given hour of the day. Given the name and address of the place.")

    def _run(self, name: str, address: str):
        """
        Runs the tool to retrieve the busyness data for a given place.

        This method interacts with an external service to obtain the popular times of the specified place.

        Args:
            name (str): The name of the place to check for busy times.
            address (str): The address of the place to check for busy times.

        Returns:
            dict: A dictionary containing the popular times data for the place.
        """
        return gs.get_populartimes_from_search(name, address)

class Food(BaseTool):
    """
    Food is a tool for finding the best places to eat based on food preference and city.

    Attributes:
        name (str): The name of the tool.
        description (str): A brief description of the tool's purpose.
    """
    name: str = "Get information where to eat"
    description: str = ("This tool helps you get information the best places to eat "
                        "Given the given the foodPreference and the city.")

    def _run(self, city, foodPreference):
        """
        Runs the tool to find recommended places to eat in a specified city based on food preference.

        This method uses an external service to search for dining options that match the given criteria.

        Args:
            city (str): The city where you want to find places to eat.
            foodPreference (str): The type of food you prefer (e.g., Italian, Chinese).

        Returns:
            list[dict]: A list of recommended places to eat that match the specified preferences.
        """
        return gs.find_place(city, foodPreference)