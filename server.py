from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from sugarscape.agents import SsAgent, Sugar
from sugarscape.model import SugarscapeSeasonalGrowback

color_dic = {4: "#005C00",
             3: "#008300",
             2: "#00AA00",
             1: "#00F800"}


def SsAgent_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is SsAgent:
        if agent.strategy==0:
            portrayal["Shape"] = "sugarscape/resources/ant0.jpeg"
        elif agent.strategy==1:
            portrayal["Shape"] = "sugarscape/resources/ant1.jpeg"
        else:
            portrayal["Shape"] = "sugarscape/resources/ant2.jpeg"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Sugar:
        if agent.amount != 0:
            portrayal["Color"] = color_dic[agent.amount]
        else:
            portrayal["Color"] = "#D6F5D6"
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(SsAgent_portrayal, 50, 50, 500, 500)
chart_element = ChartModule([{"Label": "SsAgent", "Color": "#AA0000"},{"Label": "SsAgent1", "Color": "#666666"},{"Label": "SsAgent2", "Color": "#008300"}])

model_params = {"initial_population": UserSettableParameter('slider', 'Initial Population', 100, 1, 500),
               "reproduce": UserSettableParameter('slider', 'Reproduction Rate', 0.05, 0.00, 1.0,
                                                        0.01,
                                                        description="The rate at which agents reproduce."),
               "min_metabolism": UserSettableParameter('slider', 'Min Metabolism', 1, 1, 8,
                                                        1,
                                                        description="The rate at which agents reproduce."),
               "max_metabolism": UserSettableParameter('slider', 'Max Metabolism', 5, 1, 8,
                                                        1,
                                                        description="The rate at which agents reproduce."),
               "min_vision": UserSettableParameter('slider', 'Min Vision', 1, 1, 10,
                                                        1,
                                                        description="The rate at which agents reproduce."),
               "max_vision": UserSettableParameter('slider', 'Max Vision', 5, 1, 10,
                                                        1,
                                                        description="The rate at which agents reproduce."),
               "summer_growth": UserSettableParameter('slider', 'Summer Growth', 5, 1, 10,
                                                        1,
                                                        description="The rate at which agents reproduce."),
               "winter_growth": UserSettableParameter('slider', 'Winter Growth', 15, 5, 40,
                                                        1,
                                                        description="The rate at which agents reproduce.")}

server = ModularServer(SugarscapeSeasonalGrowback, [canvas_element, chart_element],
                       "Sugarscape Seasonal Growback", model_params)
# server.launch()
