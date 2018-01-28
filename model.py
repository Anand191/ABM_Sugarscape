'''
Sugarscape Constant Growback Model
================================

Replication of the model found in Netlogo:
Li, J. and Wilensky, U. (2009). NetLogo Sugarscape 2 Constant Growback model.
http://ccl.northwestern.edu/netlogo/models/Sugarscape2ConstantGrowback.
Center for Connected Learning and Computer-Based Modeling,
Northwestern University, Evanston, IL.
'''

import random

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from sugarscape.agents import SsAgent, Sugar
from sugarscape.schedule import RandomActivationByBreed


class SugarscapeSeasonalGrowback(Model):
    '''
    Sugarscape Seasonal Growback
    '''
    reproduce=0.01
    min_vision=1
    max_vision=10
    min_metabolism=1
    max_metabolism=6
    summer_growth=2
    winter_growth=15
    verbose = True  # Print-monitoring

    def __init__(self, height=50, width=50,
                 initial_population=100,reproduce=0.01,min_vision=1,max_vision=10,min_metabolism=1,max_metabolism=6,summer_growth=2,winter_growth=15):
        '''
        Create a new Constant Growback model with the given parameters.

        Args:
            initial_population: Number of population to start with
        '''

        # Set parameters
        self.height = height
        self.width = width
        self.initial_population = initial_population
        self.reproduce=reproduce
        self.vision = random.randrange(min_vision, max_vision)
        self.metabolism = random.randrange(min_metabolism, max_metabolism)
        self.summer_growth=summer_growth
        self.winter_growth=winter_growth
        
        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=False)
        self.datacollector = DataCollector({"SsAgent": lambda m: m.schedule.get_breed_count_str0(SsAgent)
                                            ,"SsAgent1": lambda m: m.schedule.get_breed_count_str1(SsAgent)
                                            ,"SsAgent2": lambda m: m.schedule.get_breed_count_str2(SsAgent)
                                           })

        # Create sugar
        import numpy as np
        sugar_distribution = np.genfromtxt("sugarscape/sugar-map.txt")
        for _, x, y in self.grid.coord_iter():
            max_sugar = sugar_distribution[x, y]
            sugar = Sugar((x, y), self, max_sugar,summer_growth,winter_growth)
            self.grid.place_agent(sugar, (x, y))
            self.schedule.add(sugar)

        # Create agent:
        for i in range(self.initial_population):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            sugar = random.randrange(6, 12)
            metabolism = random.randrange(min_metabolism, max_metabolism)
            vision = random.randrange(min_vision, max_vision)
            maxage = random.randrange(60,100)
            age = 0
            strategy=random.randint(0,2)
            influ=random.randint(1,12)
            #influ=0
            ssa = SsAgent((x, y), self, False, sugar, metabolism, vision,strategy, maxage, age, influ)
            self.grid.place_agent(ssa, (x, y))
            self.schedule.add(ssa)

        self.running = True

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time,
                   self.schedule.get_breed_count(SsAgent)])

    def run_model(self, step_count=100):

        if self.verbose:
            print('Initial number Sugarscape Agent: ',
                  self.schedule.get_breed_count(SsAgent))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print('')
            print('Final number Sugarscape Agent: ',
                  self.schedule.get_breed_count(SsAgent))
