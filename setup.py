from tba_pull import get_matches, get_rankings


def get_matrix(event_key):  # returns a coordinate matrix that displays who played which teams

    matches = get_matches(event_key)

    team_keys = []
    rankings = get_rankings(event_key)["rankings"]
    for ranking in rankings:
        team_keys.append(ranking["team_key"][3:])   # adds all team numbers to the team_keys list
    team_keys.sort(key=int)                         # sorts team numbers numerically
    while not team_keys[0].startswith("frc"):
        element = f"frc{team_keys.pop(0)}"          # adds the "frc" back into each number to make it a key
        team_keys.append(element)                   # appends it back into list

    coefficients = []
    solutions = []
    for i in range(len(team_keys)):     # creates blank matrix
        row = []
        for j in range(len(team_keys)):
            row.append(0)
        coefficients.append(row)
        solutions.append({})

    for match in matches:                                   # fill in matrix
        if match["comp_level"] == "qm":                     # ignore bracket matches
            for alliance in match["alliances"].values():
                for i in alliance["team_keys"]:
                    row = coefficients[team_keys.index(i)]
                    for j in alliance["team_keys"]:
                        row[team_keys.index(j)] += 1

    return coefficients


get_matrix("2020gadal")
