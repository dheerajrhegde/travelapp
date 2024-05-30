import urllib.parse
import urllib.request
import json, re
import requests

# urls for google api web service
BASE_URL = "https://maps.googleapis.com/maps/api/place/"
api_key="AIzaSyDRXbm3xf9lH2Y5A7Sv97DeRhzk0-8PoRk"

USER_AGENT = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/54.0.2840.98 Safari/537.36"}


def get_populartimes_from_search(name, address):
    """
    request information for a place and parse current popularity
    :param name: name string
    :param address: address string for checking if numbered address
    :return:
    """
    place_identifier = "{} {}".format(name, address)

    params_url = {
        "tbm": "map",
        "tch": 1,
        "hl": "en",
        "q": urllib.parse.quote_plus(place_identifier),
        "pb": "!4m12!1m3!1d4005.9771522653964!2d-122.42072974863942!3d37.8077459796541!2m3!1f0!2f0!3f0!3m2!1i1125!2i976"
              "!4f13.1!7i20!10b1!12m6!2m3!5m1!6e2!20e3!10b1!16b1!19m3!2m2!1i392!2i106!20m61!2m2!1i203!2i100!3m2!2i4!5b1"
              "!6m6!1m2!1i86!2i86!1m2!1i408!2i200!7m46!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e3!2b0!3e3!"
              "1m3!1e4!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e3!2b1!3e2!1m3!1e9!2b1!3e2!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e"
              "10!2b0!3e4!2b1!4b1!9b0!22m6!1sa9fVWea_MsX8adX8j8AE%3A1!2zMWk6Mix0OjExODg3LGU6MSxwOmE5ZlZXZWFfTXNYOGFkWDh"
              "qOEFFOjE!7e81!12e3!17sa9fVWea_MsX8adX8j8AE%3A564!18e15!24m15!2b1!5m4!2b1!3b1!5b1!6b1!10m1!8e3!17b1!24b1!"
              "25b1!26b1!30m1!2b1!36b1!26m3!2m2!1i80!2i92!30m28!1m6!1m2!1i0!2i0!2m2!1i458!2i976!1m6!1m2!1i1075!2i0!2m2!"
              "1i1125!2i976!1m6!1m2!1i0!2i0!2m2!1i1125!2i20!1m6!1m2!1i0!2i956!2m2!1i1125!2i976!37m1!1e81!42b1!47m0!49m1"
              "!3b1"
    }

    search_url = "http://www.google.de/search?" + "&".join(k + "=" + str(v) for k, v in params_url.items())

    resp = urllib.request.urlopen(urllib.request.Request(url=search_url, data=None, headers=USER_AGENT))
    data = resp.read().decode('utf-8').split('/*""*/')[0]

    # find eof json
    jend = data.rfind("}")
    if jend >= 0:
        data = data[:jend + 1]

    jdata = json.loads(data)["d"]
    jdata = json.loads(jdata[4:])

    # check if proper and numeric address, i.e. multiple components and street number
    is_proper_address = any(char.isspace() for char in address.strip()) and any(char.isdigit() for char in address)

    info = index_get(jdata, 0, 1, 0 if is_proper_address else 1, 14)

    rating = index_get(info, 4, 7)
    rating_n = index_get(info, 4, 8)

    popular_times = index_get(info, 84, 0)

    time_spent = index_get(info, 117, 0)

    # extract wait times and convert to minutes
    if time_spent:

        nums = [float(f) for f in re.findall(r'\d*\.\d+|\d+', time_spent.replace(",", "."))]
        contains_min, contains_hour = "min" in time_spent, "hour" in time_spent or "hr" in time_spent

        time_spent = None

        if contains_min and contains_hour:
            time_spent = [nums[0], nums[1] * 60]
        elif contains_hour:
            time_spent = [nums[0] * 60, (nums[0] if len(nums) == 1 else nums[1]) * 60]
        elif contains_min:
            time_spent = [nums[0], nums[0] if len(nums) == 1 else nums[1]]

        time_spent = [int(t) for t in time_spent]

    return rating, rating_n, popular_times, time_spent

def index_get(array, *argv):
    """
    checks if a index is available in the array and returns it
    :param array: the data array
    :param argv: index integers
    :return: None if not available or the return value
    """

    try:

        for index in argv:
            array = array[index]

        return array

    # there is either no info available or no popular times
    # TypeError: rating/rating_n/populartimes wrong of not available
    except (IndexError, TypeError):
        return None

def find_place(city, activities):
    # Define the API endpoint
    url = 'https://places.googleapis.com/v1/places:searchText'
    # Define the headers
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,  # Replace 'API_KEY' with your actual Google Places API key
        'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress,places.websiteUri'
    }

    # Define the data payload for the POST request
    data = {'textQuery': " ".join(activities) + " in " + city }


    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Process the response
        print(response.json())
    else:
        print(f"Error: {response.status_code}, {response.text}")
    return json.loads(response.text)

def get_place_operating_hours(place_id):
    # Define the API endpoint
    url = 'https://places.googleapis.com/v1/places/'+place_id
    # Define the headers
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,  # Replace 'API_KEY' with your actual Google Places API key
        'X-Goog-FieldMask': 'currentOpeningHours'
    }

    # Make the POST request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Process the response
        print(response.json())
    else:
        print(f"Error: {response.status_code}, {response.text}")
    return json.loads(response.text)