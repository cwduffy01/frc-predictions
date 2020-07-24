from tba_pull import get_matches, get_rankings
import itertools
import collections


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
            for color in match["alliances"]:
                alliance = match["alliances"][color]
                for i in alliance["team_keys"]:

                    values = get_values(event_key, match, color)
                    Cdict = collections.defaultdict(int)

                    # combines values of each match with corresponding row in solutions
                    for key, val in itertools.chain(values.items(), solutions[team_keys.index(i)].items()):
                        Cdict[key] += val

                    solutions[team_keys.index(i)] = dict(Cdict)

                    row = coefficients[team_keys.index(i)]
                    for j in alliance["team_keys"]:
                        row[team_keys.index(j)] += 1

    return coefficients, solutions, team_keys


def get_values(event_key, match, color):

    values = {"scores": match["alliances"][color]["score"]}
    breakdown = match["score_breakdown"][color]
    year = event_key[:4]

    if year == "2020":
        values["autoCellsBottom"] = breakdown["autoCellsBottom"]
        values["autoCellsOuter"] = breakdown["autoCellsOuter"]
        values["autoCellsInner"] = breakdown["autoCellsInner"]
        values["autoCellsTotal"] = values["autoCellsBottom"] + values["autoCellsOuter"] + values["autoCellsInner"]
        values["teleopCellsBottom"] = breakdown["teleopCellsBottom"]
        values["teleopCellsOuter"] = breakdown["teleopCellsOuter"]
        values["teleopCellsInner"] = breakdown["teleopCellsInner"]
        values["teleopCellsTotal"] = values["teleopCellsBottom"] + values["teleopCellsOuter"] + \
                                     values["teleopCellsInner"]
        values["cellsTotal"] = values["teleopCellsTotal"] + values["autoCellsTotal"]
        values["percentLevel"] = int(breakdown["endgameRungIsLevel"] == "IsLevel")
        values["foulPoints"] = breakdown["foulPoints"]

    return values
