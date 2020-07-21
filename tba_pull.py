import requests

# base url of API
URL = "http://www.thebluealliance.com/api/v3"

# authorization key used of API access
AUTH_HEADERS = {}
with open("X-TBA-Auth-Key.txt", 'r') as f:
    AUTH_HEADERS["X-TBA-Auth-Key"] = f
