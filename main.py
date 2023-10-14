import  json
import matplotlib.pyplot as plt

from modules import supplementary
from modules.apiInterface import OctopusObject


with open('config.json', 'r') as file:
    conf = json.load(file)

octopusInstance = OctopusObject(**conf)

data_el = octopusInstance.get_electricity_metered()

fig = octopusInstance.plot_electricity()

fig.savefig('el_consuption_24h.png')
