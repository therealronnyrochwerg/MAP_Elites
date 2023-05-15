from parameters import Parameters
from parent_selection import select_parent

class MAPElites (object):

    # model is a reference to a class for the model (like LGP)
    def __init__(self, input_data, target_data, num_features):
        self.param = Parameters()
        self.input_data = input_data
        self.target_data = target_data

        #number of features in teh input data (needed for LGP models)
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
