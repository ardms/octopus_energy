import pandas as pd

def get_dates():
    today = pd.to_datetime('now').floor('D')

    date_start = today.to_period('M').to_timestamp()
    date_end = today - pd.Timedelta('24h')
    date_end_plot = date_start + pd.DateOffset(months=1)

    return (date_start, date_end, date_end_plot)


