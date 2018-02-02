from sugarscape.server import server
from sugarscape.model import SugarscapeSeasonalGrowback

#server.launch()
model = SugarscapeSeasonalGrowback()
model.run_model()
agent_data = model.datacollector.get_agent_vars_dataframe()
model_data = model.datacollector.get_model_vars_dataframe()
model_data.to_csv('model_data.csv',index=False)
df = agent_data[agent_data.name != 'sugar']
df.to_csv('agent_data.csv')
#df.groupby(['Step']).size().to_csv('check2.csv')