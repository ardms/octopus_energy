import pandas as pd
import requests
from dataclasses import dataclass
import matplotlib.pyplot as plt


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

    def get_electricity_metered(self, date_start, date_end) -> pd.DataFrame:
        '''
        Dowloads electricity consumption from Octopus Rest API for the given period.
        
        Returns: Pandas dataframe and saved them in self.data_el_metered
        '''
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

        Returns: Matplotlib.figure element
        '''
        df_el = self.data_el_metered

        fig, axs = plt.subplots(figsize=(10, 3))

        axs.plot(df_el.index, df_el['consumption'])

        return fig
