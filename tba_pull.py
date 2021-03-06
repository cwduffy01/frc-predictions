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


def get_events(team_key, year=None, keys=False):   # gets a list of events that a team has participated in
    if keys:                # returns only team keys
        if year is None:    # returns all events
            return requests.get(f"{URL}/team/{team_key}/events/keys", headers=AUTH_HEADERS).json()
        return requests.get(f"{URL}/team/{team_key}/events/{year}/keys", headers=AUTH_HEADERS).json()
    if year is None:        # returns only team keys
        return requests.get(f"{URL}/team/{team_key}/events", headers=AUTH_HEADERS).json()
    return requests.get(f"{URL}/team/{team_key}/events/{year}", headers=AUTH_HEADERS).json()


def get_matches(event_key):     # gets a list of information about matches at an event based on its key
    return requests.get(f"{URL}/event/{event_key}/matches", headers=AUTH_HEADERS).json()


def get_teams(event_key, keys=False):
    if keys:
        return requests.get(f"{URL}/event/{event_key}/teams/keys", headers=AUTH_HEADERS).json()
    return requests.get(f"{URL}/event/{event_key}/teams", headers=AUTH_HEADERS).json()


def get_rankings(event_key):
    return requests.get(f"{URL}/event/{event_key}/rankings", headers=AUTH_HEADERS).json()
