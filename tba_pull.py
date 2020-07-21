import requests

# base url of API
URL = "http://www.thebluealliance.com/api/v3"

# authorization key used of API access
key = open("X-TBA-Auth-Key.txt", 'r').read()
AUTH_HEADERS = {
    'X-TBA-Auth-Key': key
}


def get_event_info(event_key):
    events = requests.get(f"{URL}/event/{event_key}", headers=AUTH_HEADERS).json()
    return events
