import random
import math
import numpy as np

from mesa import Agent



def get_distance(pos_1, pos_2):
    """ Get the distance between two point

    Args:
        pos_1, pos_2: Coordinate tuples for both points.

    """
    x1, y1 = pos_1
    x2, y2 = pos_2
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx ** 2 + dy ** 2)


class SsAgent(Agent):
    def __init__(self,name, u_id, pos, model, moore=False, sugar=0, metabolism=0, vision=0,strategy=0,maxage=0,age=0,influ=0,belief =0,belief_num=3):
        super().__init__(pos, model)
        self.name = name
        self.u_id = u_id
        self.pos = pos
        self.moore = moore
        self.sugar = sugar
        self.metabolism = metabolism
        self.vision = vision
        self.strategy = strategy
        self.maxage = maxage
        self.age = age
        self.influ = influ
        self.belief=belief
        self.belief_num=belief_num
        #self.belief_num=self.model.belief_num
        #self.reproduce = reproduce

    def get_sugar(self, pos):
        this_cell = self.model.grid.get_cell_list_contents([pos])
        for agent in this_cell:
            if type(agent) is Sugar:
                return agent

    def is_occupied(self, pos):
        this_cell = self.model.grid.get_cell_list_contents([pos])
        return len(this_cell) > 1

    def move(self):
        # Get neighborhood within vision
        neighbors = [i for i in self.model.grid.get_neighborhood(self.pos, self.moore,
                False, radius=self.vision) if not self.is_occupied(i)]
        neighbors.append(self.pos)
        # Look for location with the most sugar
        max_sugar = max([self.get_sugar(pos).amount for pos in neighbors])
        candidates = [pos for pos in neighbors if self.get_sugar(pos).amount ==
                max_sugar]
        # Narrow down to the nearest ones
        min_dist = min([get_distance(self.pos, pos) for pos in candidates])
        
        max_dist = max([get_distance(self.pos, pos) for pos in candidates])
        
        
        
        
        vonneighbors = self.model.grid.get_neighbors(self.pos, self.moore,False, radius=2)
        vonn2 = [v for v in vonneighbors if v.name != 'sugar']
        # vonneighbors.append(self.pos)
        num = np.zeros(self.belief_num)
        for i in range(0,self.belief_num):
            count = 0
            for v in vonn2:
                if(v.belief == i):
                    count +=1
            num[i] = count



        if all(v == 0. for v in num):
            self.strategy = 1
        else:
            max_belief_list = []

            for i in range(self.belief_num):
                if num[i] == max(num):
                    max_belief_list.append(i)
            random.shuffle(max_belief_list)
            max_belief = max_belief_list[0]

            if (self.belief==max_belief):
                self.strategy = 0
            else:
                if (self.influ < random.random()):
                    self.strategy = 1
                else:
                    self.belief = max_belief
                    self.strategy = 0
                
       
        
            #num(candidate)
       
        #Strategy 2
        #final_candidates = candidates
        #Strategy chosen
        if (self.strategy==0):
            final_candidates = [pos for pos in candidates if get_distance(self.pos,
                pos) == min_dist]
            #final_candidates = candidates
        elif (self.strategy==1):
            final_candidates = [pos for pos in candidates if get_distance(self.pos,
                pos) == max_dist]  
            #final_candidates = candidates
        #else:
         #   final_candidates = candidates
        
        
              
        random.shuffle(final_candidates)
        self.model.grid.move_agent(self, final_candidates[0])

    def eat(self):
        sugar_patch = self.get_sugar(self.pos)
        self.sugar = self.sugar - self.metabolism + sugar_patch.amount
        sugar_patch.amount = 0        
               
        
        
    def step(self):
        self.move()
        self.eat()
        self.age = self.age + 1
        if self.age > self.maxage:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            
        elif self.sugar <= 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            
       #reproduction
        if ((self.sugar>20) and (random.random() < self.model.reproduce) and (self.age>20)):
                self.sugar = math.floor(self.sugar/2)
                cub = SsAgent(self.name, self.u_id+101 , self.pos, self.model, False, self.sugar, self.metabolism,
                          self.vision, self.strategy, random.randrange(60, 100),0, self.influ, self.belief,self.belief_num)
                #cub = SsAgent(self.pos, self.model, False, self.sugar, random.randrange(min_metabolism, max_metabolism), random.randrange(min_vision, max_vision), self.strategy, random.randrange(60,100),0,random.random(),random.randint(0,self.belief_num))
                                
                self.model.grid.place_agent(cub, cub.pos)
                self.model.schedule.add(cub)

class Sugar(Agent):
    def __init__(self, pos, model, max_sugar,summer_growth,winter_growth):
        super().__init__(pos, model)
        self.name = "sugar"
        self.amount = max_sugar
        self.max_sugar = max_sugar
        self.summer_growth = summer_growth
        self.winter_growth = winter_growth
        
        

    #Sugar Seasonal Growback
    def step(self):
        if (self.model.schedule.time % 80 <= 40):
            if ((self.pos[1]>=25) and (self.model.schedule.time%self.summer_growth==0)):
                self.amount = min([self.max_sugar, self.amount + 1])
            if (self.pos[1]<25 and (self.model.schedule.time%self.winter_growth==0)):
                self.amount = min([self.max_sugar, self.amount + 1])
        else:
            if ((self.pos[1]>=25) and (self.model.schedule.time%self.winter_growth==0)):
                self.amount = min([self.max_sugar, self.amount + 1])
            if (self.pos[1]<25 and (self.model.schedule.time%self.summer_growth==0)):
                self.amount = min([self.max_sugar, self.amount + 1])
                

