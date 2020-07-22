from tba_pull import get_matches, get_teams


def get_matrix(event_key):  # returns a coordinate matrix that displays who played which teams

    matches = get_matches(event_key)

    teams = get_teams(event_key)
    team_keys = []
    for team in teams:
        team_keys.append(team["key"])

    coefficients = []
    for i in range(len(team_keys)):
        row = []
        for j in range(len(team_keys)):
            row.append(0)
        coefficients.append(row)

    for match in matches:
        if match["comp_level"] == "qm":
            for alliance in match["alliances"].values():
                for i in alliance["team_keys"]:
                    row = coefficients[team_keys.index(i)]
                    for j in alliance["team_keys"]:
                        row[team_keys.index(j)] += 1
