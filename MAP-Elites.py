from parameters import Parameters
from parent_selection import select_parent
from random import random

class MAPElites (object):

    # model is a reference to a class for the model (like LGP)
    def __init__(self, input_data, target_data, num_features):
        self.param = Parameters()
        self.input_data = input_data
        self.target_data = target_data

        #number of features in the input data (needed for LGP models)
        self.num_features = num_features
        # dictionary where the keys are the behaviours and the values are the models and their fitness
        self.mapE = {}

    def add_individual(self, individual):
        if individual.behavior in self.mapE:
            if individual.fitness > self.mapE[individual.behavior].fitness:
                self.mapE[individual.behavior] = individual
        else:
            self.mapE[individual.behavior] = individual

    def initialize(self):
        for i in range(self.param.pop_init_amount):
            individual = self.param.model(self.num_features)
            self.add_individual(individual)

    def sim_generation(self):
        parents = select_parent(self.param,self.mapE)
        '''Do the rest of this, have to do recombination and mutation of parents to get children'''
        mutate = False
        # going through all selected parents to create offspring for the generation
        while parents:
            # choosing between mutation or recombination
            if mutate or len(parents) == 1 or random() > self.param.recom_rate:
                p1 = parents.pop(0)
                c1 = p1.mutate_child()
                self.add_individual(c1)
            else:
                p1 = parents.pop(0)
                # if all the remaining parents are the same individual, force mutation for all remaining
                if parents.count(p1) == len(parents):
                    mutate = True
                    c1 = p1.mutate_child()
                    self.add_individual(c1)
                else:
                    p2 = parents.pop(0)

                    # if the two selected parents are the same keep searching for a different parent
                    while p1 == p2:
                        parents.append(p2)
                        p2 = parents.pop(0)