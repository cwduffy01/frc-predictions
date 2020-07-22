from tba_pull import get_matches, get_teams


def get_matrix(event_key):  # returns a coordinate matrix that displays who played which teams

    matches = get_matches(event_key)

    teams = get_teams(event_key)
    team_keys = []
    for team in teams:
        team_keys.append(team["key"])

    matrix = []
