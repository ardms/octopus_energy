import  json
import matplotlib.pyplot as plt

from modules import supplementary
from modules.apiInterface import OctopusObject


with open('config.json', 'r') as file:
    conf = json.load(file)

octopusInstance = OctopusObject(**conf)

date_start, date_end = supplementary.get_dates()
data_el = octopusInstance.get_electricity_metered(date_start, date_end)

fig = octopusInstance.plot_electricity()

fig.savefig('el_consuption_24h.png')
