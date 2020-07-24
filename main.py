import pandas as pd
import os

from predict import predict
from tba_pull import get_events


def predict_event(event_key):

    path = f"event_predictions/{event_key[:4]}"

    try:
        df = pd.read_csv(f"{path}/{event_key}.csv")
    except FileNotFoundError:                                   # if csv file doesn't exist
        df = predict(event_key)                                 # predict event
        try:
            df.to_csv(f"{path}/{event_key}.csv")
        except FileNotFoundError:                               # if directory for event year doesn't exist
            os.makedirs(path)                                      # create directory
            df.to_csv(f"{path}/{event_key}.csv")    # create csv file

    return df
