import pandas as pd
import os

from predict import predict
from tba_pull import get_events, get_rankings


def get_event_prediction(event_key):

    path = f"event_predictions/{event_key[:4]}"

    try:
        df = pd.read_csv(f"{path}/{event_key}.csv")
        df.set_index("teamKey", inplace=True, drop=True)
    except FileNotFoundError:                                   # if csv file doesn't exist
        df = predict(event_key)                                 # predict event
        try:
            df.to_csv(f"{path}/{event_key}.csv")
        except FileNotFoundError:                               # if directory for event year doesn't exist
            os.makedirs(path)                                      # create directory
            df.to_csv(f"{path}/{event_key}.csv")    # create csv file

    return df


def get_team_predictions(team_key, *years, offseason=False):

    events = []
    for year in years:
        events.extend(get_events(team_key, year))   # extend each year's list of events
    if len(years) == 0:
        events = get_events(team_key, None)         # get all events if none specified

    event_dfs = []
    for event in events:
        if event["event_type"] != 4:    # doesn't count einstein
            if event["event_type"] not in [99, 100] or offseason:       # count offseason events if specified
                if len(get_rankings(event["key"])["rankings"]) != 0:    # if event has happened already
                    event_df = get_event_prediction(event["key"]).loc[[team_key]]   # isolate single row for team
                    event_df["eventKey"] = pd.Series([event["key"]], index=event_df.index)  # add eventKey series
                    event_df.set_index("eventKey", inplace=True, drop=True)         # change index to eventKey
                    event_dfs.append(event_df)

    df = pd.concat(event_dfs)   # merge all DataFrames
    return df


print(get_team_predictions("frc4910", 2019, 2018, offseason=True))
