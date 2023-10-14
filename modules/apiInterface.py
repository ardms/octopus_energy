import pandas as pd
import requests
from dataclasses import dataclass
import matplotlib.pyplot as plt
from modules.supplementary import get_dates


@dataclass
class OctopusObject:
    "Stores all infomration including any data that have been downloaded"
    name: str
    url_base: str
    token: str
    electricity_mpan: str
    electricity_sn: str
    gas_mprn: str
    gas_sn: str
    # All outputs
    data_el_metered: pd.DataFrame = pd.DataFrame()
    data_gas_metered: pd.DataFrame = pd.DataFrame()

    date_start, date_end, date_end_plot = pd.Timestamp = get_dates()

    def get_electricity_metered(self) -> pd.DataFrame:
        '''
        Dowloads electricity consumption from Octopus Rest API for the given period.
        
        Returns: Pandas dataframe and saved them in self.data_el_metered
        '''
        date_start = self.date_start
        date_end = self.date_end

        url = f'{self.url_base}electricity-meter-points/' \
                + f'{self.electricity_mpan}/meters/' \
                + f'{self.electricity_sn}/consumption/'
        params = {'period_from': date_start,
                  'period_to': date_end,
                  'page_size': 25000
                  }
        request = requests.get(url, params=params, auth=(self.token, ''))
        data = pd.DataFrame(request.json()['results'])
        data['interval_start'] = pd.to_datetime(data['interval_start'])
        data['interval_end'] = pd.to_datetime(data['interval_end'])
        data.index = data['interval_start']
        self.data_el_metered = data
        return data

    def plot_electricity(self): 
        '''
        Uses electricity data to plot a line plot using matplotlid

        Returns: Matplotlib.figure.Figure element
        '''
        index = pd.date_range(self.date_start, self.date_end_plot, freq='1D', tz='Europe/London')

        df_el = self.data_el_metered.resample('D')[['consumption']].sum()
        df_el = df_el.reindex(index)
        df_el['cumsum'] = df_el['consumption'].cumsum(skipna=False)
        df_el['cumsum_pred'] = df_el['cumsum'].interpolate(method='slinear', limit=40)

        # df_el.fillna(0, inplace=True)


        fig, (ax1, ax2) = plt.subplots(ncols=1, nrows=2, figsize=(10, 6), sharex=True)

        ax1.bar(df_el.index, df_el['consumption'])
        ax2.plot(df_el.index, df_el['cumsum'])

        return fig
