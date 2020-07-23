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
        solutions[category] = list(np.linalg.solve(np.array(a), np.array(b)))

    return pd.DataFrame(solutions, index=data[2])   # return pandas DataFrame of predicted data
