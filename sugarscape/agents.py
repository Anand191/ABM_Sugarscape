import random
import math

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
    def __init__(self, pos, model, moore=False, sugar=0, metabolism=0, vision=0,strategy=0,maxage=0,age=0):
        super().__init__(pos, model)
        self.pos = pos
        self.moore = moore
        self.sugar = sugar
        self.metabolism = metabolism
        self.vision = vision
        self.strategy = strategy
        self.maxage = maxage
        self.age = age
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
        
        #Strategy chosen
        #if (self.strategy==0):
         #   final_candidates = [pos for pos in candidates if get_distance(self.pos,
          #      pos) == min_dist]
        #else:
         #   final_candidates = [pos for pos in candidates if get_distance(self.pos,
          #      pos) == max_dist]
        
        #Strategy 2
        final_candidates = candidates
        
        
        
              
        random.shuffle(final_candidates)
        self.model.grid.move_agent(self, final_candidates[0])

    def eat(self):
        sugar_patch = self.get_sugar(self.pos)
        self.sugar = self.sugar - self.metabolism + sugar_patch.amount
        sugar_patch.amount = 0
        self.age = self.age + 1

    def step(self):
        self.move()
        self.eat()
        if self.age > self.maxage:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            
        elif self.sugar <= 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            
       #reproduction
        if ((self.sugar>20) and (random.random() < self.model.reproduce)):
                self.sugar = math.floor(self.sugar/2)
                cub = SsAgent(self.pos, self.model, False, self.sugar, self.metabolism, self.vision, self.strategy, random.randrange(60,100))
                #cub = SsAgent(self.pos, self.model, False, self.sugar, random.randrange(1, 5), random.randrange(1, 6), self.strategy, random.randrange(60,100))
                self.model.grid.place_agent(cub, cub.pos)
                self.model.schedule.add(cub)

class Sugar(Agent):
    def __init__(self, pos, model, max_sugar):
        super().__init__(pos, model)
        self.amount = max_sugar
        self.max_sugar = max_sugar

    #Sugar Seasonal Growback
    def step(self):
        if (self.model.schedule.time % 60 <= 30):
            if ((self.pos[1]>=25) and (self.model.schedule.time%2==0)):
                self.amount = min([self.max_sugar, self.amount + 1])
            if (self.pos[1]<25 and (self.model.schedule.time%15==0)):
                self.amount = min([self.max_sugar, self.amount + 1])
        else:
            if ((self.pos[1]>=25) and (self.model.schedule.time%15==0)):
                self.amount = min([self.max_sugar, self.amount + 1])
            if (self.pos[1]<25 and (self.model.schedule.time%2==0)):
                self.amount = min([self.max_sugar, self.amount + 1])
                
