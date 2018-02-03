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
import pandas as pd
import numpy as np

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from sugarscape.agents import SsAgent, Sugar
from sugarscape.schedule import RandomActivationByBreed


class SugarscapeSeasonalGrowback(Model):
    '''
    Sugarscape Seasonal Growback
    '''
    reproduce = 0.01
    belief_num = 3
    min_vision = 1
    max_vision = 10
    min_metabolism = 1
    max_metabolism = 6
    summer_growth = 2
    winter_growth = 15
    verbose = True  # Print-monitoring

    def __init__(self, height=50, width=50,
                 initial_population=100, reproduce=0.05, min_vision=1, max_vision=10, min_metabolism=1,
                 max_metabolism=6, summer_growth=2, winter_growth=15, belief_num=3):
        '''
        Create a new Constant Growback model with the given parameters.

        Args:
            initial_population: Number of population to start with
        '''

        # Set parameters
        self.height = height
        self.width = width
        self.initial_population = initial_population
        self.reproduce = reproduce
        self.belief_num=belief_num
        self.belief = random.randrange(0, belief_num)
        self.vision = random.randrange(min_vision, max_vision)
        self.metabolism = random.randrange(min_metabolism, max_metabolism)
        self.summer_growth = summer_growth
        self.winter_growth = winter_growth

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=False)
        self.datacollector = DataCollector({"SsAgent": lambda m: m.schedule.get_breed_count_str0(SsAgent)
                                               , "SsAgent1": lambda m: m.schedule.get_breed_count_str1(SsAgent)
                                               , "SsAgent2": lambda m: m.schedule.get_breed_count_str2(SsAgent)
                                               , "SsAgent3": lambda m: m.schedule.get_breed_count_str3(SsAgent)
                                               , "SsAgent4": lambda m: m.schedule.get_breed_count_str4(SsAgent)
                                               , "SsAgent5": lambda m: m.schedule.get_breed_count_str5(SsAgent)
                                               , "SsAgent6": lambda m: m.schedule.get_breed_count_str6(SsAgent)
                                               , "SsAgent7": lambda m: m.schedule.get_breed_count_str7(SsAgent)
                                               , "SsAgent8": lambda m: m.schedule.get_breed_count_str8(SsAgent)
                                               , "SsAgent9": lambda m: m.schedule.get_breed_count_str9(SsAgent)
                                            },

                                           {"name": lambda a:a.name,
                                            "position": lambda a:a.pos,
                                           "sugar": lambda a:a.sugar,
                                           "metabolism": lambda a:a.metabolism,
                                            "vision": lambda a:a.vision,
                                            "strategy": lambda a:a.strategy,
                                            "belief":lambda a:a.belief})

        # Create sugar
        import numpy as np
        sugar_distribution = np.genfromtxt("sugarscape/sugar-map.txt")
        z = 1000
        for _, x, y in self.grid.coord_iter():
            max_sugar = sugar_distribution[x, y]
            sugar = Sugar(z, (x, y), self, max_sugar)
            self.grid.place_agent(sugar, (x, y))
            self.schedule.add(sugar)
            z +=1

        # Create agent:
        for i in range(self.initial_population):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            sugar = random.randrange(6, 25)
            metabolism = random.randrange(1, 5)
            vision = random.randrange(1, 10)
            maxage = random.randrange(60,100)
            age = 0
            strategy=random.randint(0,1)
            influ = random.random()
            belief = random.randint(0, self.belief_num-1)
            if(strategy==0):
                name = 'a0'
            else:
                name = 'a1'
            ssa = SsAgent(name, i+1, (x, y), self, False, sugar, metabolism, vision,strategy, maxage, age, influ, belief,belief_num)
            self.grid.place_agent(ssa, (x, y))
            self.schedule.add(ssa)

        self.running = True

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

        # if self.verbose:
        #     print([self.schedule.time,
        #            self.schedule.get_breed_count(SsAgent)])

    def run_model(self, step_count=100, idx=1):

        if self.verbose:
            print('Initial number Sugarscape Agent: ',
                  self.schedule.get_breed_count(SsAgent))
        sd = np.zeros((step_count, 2))
        master = []
        for i in range(step_count):
            self.step()
            slave = []
            for agent in self.schedule.agents:
                temp = []
                temp.extend((i,agent.u_id,agent.name,agent.pos,agent.sugar,agent.metabolism,agent.vision,agent.strategy, agent.influ,agent.belief))
                slave.append(temp)
            master.append(slave)

            sd[i,0] = self.schedule.time
            sd[i,1] = self.schedule.get_breed_count(SsAgent)
        cdim = len(master[0][0])
        rdim = 0
        for m in master:
            rdim += len(m)
        feature_list = ["Step","AgentID","name","position","sugar","metabolism","vision","strategy","influenciability","belief"]
        master_arr = np.zeros((rdim,cdim),dtype=object)
        start = 0
        for i in range(len(master)):
            master_arr[start:start+len(master[i])] = master[i]
            start = start+len(master[i])

        df3 = pd.DataFrame(master_arr,columns=feature_list)
        df3 = df3[df3.name != 'sugar']
        df3.to_csv('agent_data{}.csv'.format(idx),index=False)
        # df2 = pd.DataFrame(sd,columns=['time', 'agents alive'])
        # df2.to_csv('check1.csv')

        if self.verbose:
            print('')
            print('Final number Sugarscape Agent: ',
                  self.schedule.get_breed_count(SsAgent))

        #self.datacollector.get_agent_vars_dataframe().to_csv('data.csv')




