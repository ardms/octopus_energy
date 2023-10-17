import  json

from modules.apiInterface import OctopusObject


with open('config.json', 'r') as file:
    conf = json.load(file)

octopusInstance = OctopusObject(**conf)

data_el = octopusInstance.get_electricity_metered()

fig = octopusInstance.plot_electricity_monthly()

fig.savefig('el_consuption_monthly.png')
