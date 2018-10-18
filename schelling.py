#!/usr/bin/python3
import matplotlib.pyplot as plt
import itertools
import random
import copy

# This is taken from
# https://www.binpress.com/simulating-segregation-with-python/


class Schelling:
    def __init__(self, width, height, empty_ratio, similarity_threshold, n_iterations, races = 2):
        self.width = width
        self.height = height
        self.races = races
        self.empty_ratio = empty_ratio
        self.similarity_threshold = similarity_threshold
        self.n_iterations = n_iterations
        self.empty_houses = []
        self.agents = {}
        
# The populate method is used at the beginning of the simulation. This method randomly distributes people in the grid.

    def populate(self):
        self.all_houses = list(itertools.product(range(self.width),range(self.height)))
        random.shuffle(self.all_houses)
     
        self.n_empty = int( self.empty_ratio * len(self.all_houses) )
        self.empty_houses = self.all_houses[:self.n_empty]
     
        self.remaining_houses = self.all_houses[self.n_empty:]
        houses_by_race = [self.remaining_houses[i::self.races] for i in range(self.races)]
        for i in range(self.races):
            #create agents for each race
            self.agents.update(
                                dict(zip(houses_by_race[i], [i+1]*len(houses_by_race[i]))).items()
                            )
# The is_unsatisfied method takes the (x, y) coordinates of a house as arguments, checks the ratio of neighbors of similar color, and returns True if the ratio is above the happiness threshold, otherwise it returns False.

    def is_unsatisfied(self, x, y):
     
        race = self.agents[(x,y)]
        count_similar = 0
        count_different = 0
     
        if x > 0 and y > 0 and (x-1, y-1) not in self.empty_houses:
            if self.agents[(x-1, y-1)] == race:
                count_similar += 1
            else:
                count_different += 1
        if y > 0 and (x,y-1) not in self.empty_houses:
            if self.agents[(x,y-1)] == race:
                count_similar += 1
            else:
                count_different += 1
        if x < (self.width-1) and y > 0 and (x+1,y-1) not in self.empty_houses:
            if self.agents[(x+1,y-1)] == race:
                count_similar += 1
            else:
                count_different += 1
        if x > 0 and (x-1,y) not in self.empty_houses:
            if self.agents[(x-1,y)] == race:
                count_similar += 1
            else:
                count_different += 1        
        if x < (self.width-1) and (x+1,y) not in self.empty_houses:
            if self.agents[(x+1,y)] == race:
                count_similar += 1
            else:
                count_different += 1
        if x > 0 and y < (self.height-1) and (x-1,y+1) not in self.empty_houses:
            if self.agents[(x-1,y+1)] == race:
                count_similar += 1
            else:
                count_different += 1        
        if x > 0 and y < (self.height-1) and (x,y+1) not in self.empty_houses:
            if self.agents[(x,y+1)] == race:
                count_similar += 1
            else:
                count_different += 1        
        if x < (self.width-1) and y < (self.height-1) and (x+1,y+1) not in self.empty_houses:
            if self.agents[(x+1,y+1)] == race:
                count_similar += 1
            else:
                count_different += 1
     
        if (count_similar+count_different) == 0:
            return False
        else:
            return float(count_similar)/(count_similar+count_different) < self.similarity_threshold

# The update method checks if each person in the grid is unsatisfied, if yes it assigns the person to a randomly chosen empty house. It runs this process n_iterations times.

    def update(self):
        for i in range(self.n_iterations):
            self.old_agents = copy.deepcopy(self.agents)
            n_changes = 0
            for agent in self.old_agents:
                if self.is_unsatisfied(agent[0], agent[1]):
                    agent_race = self.agents[agent]
                    empty_house = random.choice(self.empty_houses)
                    self.agents[empty_house] = agent_race
                    del self.agents[agent]
                    self.empty_houses.remove(empty_house)
                    self.empty_houses.append(agent)
                    n_changes += 1
            print (n_changes)
            if n_changes == 0:
                break

#The move_to_empty method takes the (x, y) coordinates of a house as arguments, and moves the person living in the (x, y) house to an empty house. This method is called within the updatemethod to move the unsatisfied people to empty houses.

    def move_to_empty(self, x, y):
        race = self.agents[(x,y)]
        empty_house = random.choice(self.empty_houses)
        self.updated_agents[empty_house] = race
        del self.updated_agents[(x, y)]
        self.empty_houses.remove(empty_house)
        self.empty_houses.append((x, y))

#The plot method is used to draw the whole city and people living in the city. We can call this method at anytime to check the distribution of people in the city. This method takes two arguments, titleand file_name.

    def plot(self, title, file_name):
        fig, ax = plt.subplots()
        #If you want to run the simulation with more than 7 colors, you should set agent_colors accordingly
        agent_colors = {1:'b', 2:'r', 3:'g', 4:'c', 5:'m', 6:'y', 7:'k'}
        for agent in self.agents:
            ax.scatter(agent[0]+0.5, agent[1]+0.5, color=agent_colors[self.agents[agent]])
     
        ax.set_title(title, fontsize=10, fontweight='bold')
        ax.set_xlim([0, self.width])
        ax.set_ylim([0, self.height])
        ax.set_xticks([])
        ax.set_yticks([])
        plt.savefig(file_name)
        

# Now that we have our implementation of the Schelling class, we can
# run different simulations and plot the results. We’ll build three
# simulations with the following characteristics:

#    width = 50, and height = 50 (2500 houses)
#    30% of empty houses
#    Similarity Threshold = 30% (for Simulation 1), Similarity Threshold = 50% (for Simulation 2), and Similarity Threshold = 70% (for Simulation 3)
#    Maximum number of iterations = 500
#    Number of races = 2

# We start by creating and populating the cities.


schelling_1 = Schelling(50, 50, 0.3, 0.3, 500, 2)
schelling_1.populate()

schelling_2 = Schelling(50, 50, 0.3, 0.5, 500, 2)
schelling_2.populate()

schelling_3 = Schelling(50, 50, 0.3, 0.7, 500, 2)
schelling_3.populate()

#Next, we plot the city at the initial phase. Note that the Similarity threshold has no effect on the initial state of the city.

schelling_1.plot('Schelling Model with 2 colors: Initial State', 'schelling_2_initial.png')

plt.show()

# Next, we run the update method, and plot the final distribution for both Similarity thresholds.

schelling_1.update()
     
schelling_1.plot('Schelling Model with 2 colors: Final State with Similarity Threshold 30%', 'schelling_2_30_final.png')

schelling_2.update()
schelling_2.plot('Schelling Model with 2 colors: Final State with Similarity Threshold 50%', 'schelling_2_50_final.png')

schelling_3.update()
schelling_3.plot('Schelling Model with 2 colors: Final State with Similarity Threshold 70%', 'schelling_2_80_final.png')

plt.show()
