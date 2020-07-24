from predict import predict
import pandas as pd
import os


def predict_event(event_key):

    path = f"{event_key[:4]}_predictions"

    try:
        df = pd.read_csv(f"{path}/{event_key}_predictions.csv")
    except FileNotFoundError:                                   # if csv file doesn't exist
        df = predict(event_key)                                 # predict event
        try:
            df.to_csv(f"{path}/{event_key}_predictions.csv")
        except FileNotFoundError:                               # if directory for event year doesn't exist
            os.mkdir(path)                                      # create directory
            df.to_csv(f"{path}/{event_key}_predictions.csv")    # create csv file

    return df
