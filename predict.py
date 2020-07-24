from setup import get_matrix
import numpy as np
import pandas as pd


def predict(event_key):

    data = get_matrix(event_key)
    a = data[0]
    values = data[1]
    categories = values[0].keys()   # list of measures that were pulled from TBA
    solutions = {}                  # dictionary of lists of solutions corresponding to each category

    for category in categories:     # solve matrix for each category and store solutions
        b = []
        [b.append(row[category]) for row in values]
        if type(b[0]) == int:   # metric is alliance-based
            solutions[category] = list(np.linalg.solve(np.array(a), np.array(b)))   # solve matrix
        else:                   # metric is team-based
            solutions[category] = []
            [solutions[category].append(value/a[0][0]) for value in b]  # take average for each team

    df = pd.DataFrame(solutions)                        # return pandas DataFrame of predicted data
    df["teamKey"] = pd.Series(data[2])
    df.set_index("teamKey", inplace=True, drop=True)    # makes teamKeys the index
    return df
