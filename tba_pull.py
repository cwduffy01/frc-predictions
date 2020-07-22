import requests

# base url of API
URL = "http://www.thebluealliance.com/api/v3"

# authorization key used of API access
key = open("X-TBA-Auth-Key.txt", 'r').read()
AUTH_HEADERS = {
    'X-TBA-Auth-Key': key
}


def get_event(event_key):  # gets information about an event based on its key
    return requests.get(f"{URL}/event/{event_key}", headers=AUTH_HEADERS).json()


def get_matches(event_key):     # gets a list of information about matches at an event based on its key
    return requests.get(f"{URL}/event/{event_key}/matches", headers=AUTH_HEADERS).json()


def get_teams(event_key):
    return requests.get(f"{URL}/event/{event_key}/teams", headers=AUTH_HEADERS).json()


def get_rankings(event_key):
    return requests.get(f"{URL}/event/{event_key}/rankings", headers=AUTH_HEADERS).json()
