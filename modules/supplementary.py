import pandas as pd

def get_dates():
    today = pd.to_datetime('now').floor('D')

    date_end = today - pd.Timedelta('24h')
    date_start = date_end - pd.Timedelta('24h')

    return (date_start, date_end)


