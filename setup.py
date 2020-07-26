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

                    values = get_values(event_key, match, color, i)
                    Cdict = collections.defaultdict(int)
                    # combines values of each match with corresponding row in solutions
                    for key, val in itertools.chain(values.items(), solutions[team_keys.index(i)].items()):
                        Cdict[key] += val
                    solutions[team_keys.index(i)] = dict(Cdict)

                    row = coefficients[team_keys.index(i)]
                    for j in alliance["team_keys"]:
                        row[team_keys.index(j)] += 1

    return coefficients, solutions, team_keys


def get_values(event_key, match, color, team):

    """
    IMPORTANT NOTE:
        For any metrics that pertain to an individual robot
        rather than the entire alliance, cast that metric to
        a float rather than an integer. By doing this, the
        calculation function will instead take the average
        over all matches then find a solution using numpy.
        linalg.solve(), which will yield more accurate data.
    """

    breakdown = match["score_breakdown"][color]
    year = event_key[:4]
    robot_index = match["alliances"][color]["team_keys"].index(team)    # Robot 1, 2, or 3
    metrics = {"score": match["alliances"][color]["score"], "autoPoints": breakdown["autoPoints"]}

    if year == "2020":

        # AUTONOMOUS METRICS
        metrics["percentInitLine"] = float(breakdown[f"initLineRobot{robot_index + 1}"] == "Exited")
        metrics["autoCellsBottom"] = breakdown["autoCellsBottom"]
        metrics["autoCellsOuter"] = breakdown["autoCellsOuter"]
        metrics["autoCellsInner"] = breakdown["autoCellsInner"]
        metrics["autoCellsTotal"] = metrics["autoCellsBottom"] + metrics["autoCellsOuter"] + metrics["autoCellsInner"]

        # TELEOP/POWER CELL METRICS
        metrics["teleopCellsBottom"] = breakdown["teleopCellsBottom"]
        metrics["teleopCellsOuter"] = breakdown["teleopCellsOuter"]
        metrics["teleopCellsInner"] = breakdown["teleopCellsInner"]
        metrics["teleopCellsTotal"] = metrics["teleopCellsBottom"] + metrics["teleopCellsOuter"] + \
                                     metrics["teleopCellsInner"]
        metrics["cellsTotal"] = metrics["teleopCellsTotal"] + metrics["autoCellsTotal"]

        # CONTROL PANEL METRICS
        metrics["percentStage1"] = int(breakdown["stage1Activated"])
        metrics["percentStage2"] = int(breakdown["stage2Activated"])
        metrics["percentStage3"] = int(breakdown["stage3Activated"])

        # ENDGAME METRICS
        metrics["percentPark"] = float(breakdown[f"endgameRobot{robot_index+1}"] == "Park")
        metrics["percentHang"] = float(breakdown[f"endgameRobot{robot_index+1}"] == "Hang")
        metrics["percentLevel"] = int(breakdown["endgameRungIsLevel"] == "IsLevel")

    elif year == "2019":

        # SANDSTORM METRICS
        metrics["percentStartLevel1"] = float(breakdown[f"preMatchLevelRobot{robot_index + 1}"] == "HabLevel1")
        metrics["percentStartLevel2"] = float(breakdown[f"preMatchLevelRobot{robot_index + 1}"] == "HabLevel2")
        metrics["percentSandstormHABLine"] = float(breakdown[f"habLineRobot{robot_index + 1}"]
                                                  == "CrossedHabLineInSandstorm")
        metrics["percentTeleopHABLine"] = float(breakdown[f"habLineRobot{robot_index + 1}"] == "CrossedHabLineInTeleop")

        # ROCKET METRICS
        for piece in ["Panel", "Cargo"]:
            suffix = ""
            if piece == "Panel":
                suffix = 's'
            total = 0
            for level in ["low", "mid", "top"]:
                metrics[f"{level}Rocket{piece}{suffix}"] = 0
                for side in ["Right", "Left"]:
                    for location in ["Near", "Far"]:
                        metrics[f"{level}Rocket{piece}{suffix}"] += int(
                            piece in breakdown[f"{level}{side}Rocket{location}"])
                        total += int(piece in breakdown[f"{level}{side}Rocket{location}"])
            metrics[f"totalRocket{piece}{suffix}"] = total
        metrics["percentCompletedRocketNear"] = int(breakdown["completedRocketNear"])  # Rocket by scoring table
        metrics["percentCompletedRocketFar"] = int(breakdown["completedRocketFar"])  # Rocket by audience
        metrics["percentCompletedRocket"] = metrics["percentCompletedRocketNear"] + metrics["percentCompletedRocketFar"]

        # BAY METRICS
        for piece in ["Panel", "Cargo"]:
            suffix = ""
            if piece == "Panel":
                suffix = 's'
            metrics[f"totalBay{piece}{suffix}"] = 0
            for i in range(1, 9):
                metrics[f"totalBay{piece}{suffix}"] += int(piece in breakdown[f"bay{i}"])

        # PIECE METRICS
        metrics["totalPanels"] = metrics["totalRocketPanels"] + metrics["totalBayPanels"]
        metrics["totalCargo"] = metrics["totalRocketCargo"] + metrics["totalBayCargo"]
        metrics["totalPieces"] = metrics["totalPanels"] + metrics["totalCargo"]

        # ENDGAME METRICS
        metrics["percentClimbLevel1"] = float(breakdown[f"endgameRobot{robot_index + 1}"] == "HabLevel1")
        metrics["percentClimbLevel2"] = float(breakdown[f"endgameRobot{robot_index + 1}"] == "HabLevel2")
        metrics["percentClimbLevel3"] = float(breakdown[f"endgameRobot{robot_index + 1}"] == "HabLevel3")

    # FOUL METRICS
    metrics["foulCount"] = breakdown["foulCount"]
    metrics["techFoulCount"] = breakdown["techFoulCount"]
    metrics["totalFoulCount"] = metrics["foulCount"] + metrics["techFoulCount"]

    return metrics
