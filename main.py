# EXTERNAL PACKAGES
import pandas as pd
import os

# MODULES
from predict import predict
from tba_pull import get_events, get_rankings, get_teams


def get_event_predictions(event_key, overwrite=False):

    path = f"predictions/event/{event_key[:4]}"
    filename = event_key

    try:    # try opening csv file with predictions
        if overwrite:   # raise error if csv file needs to be rewritten
            raise FileNotFoundError
        df = pd.read_csv(f"{path}/{filename}.csv")
        df.set_index("teamKey", inplace=True, drop=True)

    except FileNotFoundError:       # if predictions have not been made yet

        df = predict(event_key)     # predict event

        try:    # try writing csv to path
            df.to_csv(f"{path}/{filename}.csv")

        except FileNotFoundError:                  # if path doesn't exist
            os.makedirs(path)                      # create directory
            df.to_csv(f"{path}/{filename}.csv")    # create csv file

    return df


def get_team_predictions(team_key, *years, offseason=False, overwrite=False):

    years = list(years)     # convert tuple to list
    years.sort()
    years = [str(year) for year in years]

    path = f"predictions/team/{team_key}"
    filename = f"{'_'.join(years)}{'_os' if offseason else ''}"

    try:    # try opening csv file with predictions
        if overwrite:   # raise error if csv file needs to be rewritten
            raise FileNotFoundError
        df = pd.read_csv(f"{path}/{filename}.csv")
        df.set_index("eventKey", inplace=True, drop=True)

    except FileNotFoundError:   # if predictions have not been made yet

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
                        event_df = get_event_predictions(event["key"], overwrite).loc[[team_key]]   # isolate single row for team
                        event_df["eventKey"] = pd.Series([event["key"]], index=event_df.index)  # add eventKey series
                        event_df.set_index("eventKey", inplace=True, drop=True)         # change index to eventKey
                        event_dfs.append(event_df)
        df = pd.concat(event_dfs)   # merge all DataFrames

        try:    # try writing csv to path
            df.to_csv(f"{path}/{filename}.csv")

        except FileNotFoundError:                  # if path doesn't exist
            os.makedirs(path)                      # create directory
            df.to_csv(f"{path}/{filename}.csv")    # create csv file

    return df


def get_team_list_predictions(future_event_key, overwrite=False):    # returns best scores for each team at an upcoming event

    if len(get_rankings(future_event_key)["rankings"]) != 0:    # if event has already occurred
        print("Event has already occurred")
        return get_event_predictions(future_event_key, overwrite)

    path = f"predictions/future_event/{future_event_key[:4]}"
    filename = future_event_key

    try:                # try opening csv file with predictions
        if overwrite:   # raise error if csv file needs to be rewritten
            raise FileNotFoundError
        df = pd.read_csv(f"{path}/{filename}.csv")
        df.set_index("teamKey", inplace=True, drop=True)

    except FileNotFoundError:

        team_keys = get_teams(future_event_key, keys=True)          # get team keys and sort
        team_keys = sorted(team_keys, key=lambda i: int(i[3:]))
        dfs = []

        for team_key in team_keys:

            events = get_events(team_key, year=future_event_key[:4])    # get list of events
            events = sorted(events, key=lambda i: i["start_date"])      # sort by start date
            event_keys = [event["key"] for event in events]             # get list of event keys
            del event_keys[event_keys.index(future_event_key):]         # slice list to events before predicted event

            event_dfs = []
            for event_key in event_keys:
                if team_key in [ranking["team_key"] for ranking in get_rankings(event_key)["rankings"]]:    # if team competed
                    event_dfs.append(get_event_predictions(event_key, overwrite).loc[[team_key]])  # get each event row

            if len(event_dfs) != 0:
                event_df = pd.concat(event_dfs)     # combine
                min_df = event_df[["foulCount", "techFoulCount", "totalFoulCount"]].min().to_frame().transpose()
                event_df = event_df.max().to_frame().transpose()    # get max scores over all events
                event_df.update(min_df)                             # modify fouls columns for minimum fouls
                event_df["teamKey"] = team_key
                event_df.set_index("teamKey", inplace=True)         # change index to team key
                dfs.append(event_df)

        df = pd.concat(dfs)     # merge all dataframes

        try:  # try writing csv to path
            df.to_csv(f"{path}/{filename}.csv")

        except FileNotFoundError:                # if path doesn't exist
            os.makedirs(path)                    # create directory
            df.to_csv(f"{path}/{filename}.csv")  # create csv file

    return df
