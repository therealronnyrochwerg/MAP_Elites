from parameters import Parameters
from parent_selection import select_parent
from random import random
from centroids import create_centroids, closest_centroid, shift_centroid

class MAPElites (object):

    # model is a reference to a class for the model (like LGP)
    def __init__(self, input_data, target_data, num_features, num_samples):
        self.param = Parameters()
        self.input_data = input_data
        self.target_data = target_data

        #number of features in the input data (needed for LGP models)
        self.num_features = num_features

        # the number of samples in the input data (sued for behavior vector size)
        self.num_samples = num_samples

        # dictionary where the keys are the behaviours and the values are the models and their fitness
        self.mapE = {}

    def add_individual(self, individual):
        # if the type is regular map elites
        if self.param.type == 'reg':
            # check if there is already an individual with the same behavior
            if individual.behavior in self.mapE:
                # if new individual has better fitness replace it
                if individual.fitness > self.mapE[individual.behavior].fitness:
                    self.mapE[individual.behavior] = individual
            else:
                # if there is no individual, add the new one
                self.mapE[individual.behavior] = individual

        # if the type is CVT map elites
        elif self.param.type == "CVT":
            # find the centroid the individual is closest to
            chosen_centroid = closest_centroid(self.param.centroids, individual.behavior)
            # if there is already an individual in the niche
            if self.mapE[chosen_centroid]:
                # if the new individual has higher fitness
                if individual.fitness > self.mapE[chosen_centroid].fitness:
                    # replace the old individual and shift the centroid according the new behavior
                    self.mapE[chosen_centroid] = individual
                    self.param.centroids[chosen_centroid] = shift_centroid(self.param.centroids[chosen_centroid], individual.behavior)
            else:
                # if there is no individual, add and shift
                self.mapE[chosen_centroid] = individual
                self.param.centroids[chosen_centroid] = shift_centroid(self.param.centroids[chosen_centroid],
                                                                       individual.behavior)
        else:
            quit("incompatible type in parameters")

    # used for initialization (gen 0)
    def initialize(self):
        # if type is CVT have to initialize the centroids
        if self.param.type == "CVT":
            self.mapE = dict.fromkeys(range(self.param.num_niches))
            self.param.centroids = create_centroids(self.param.num_niches, self.num_samples, seed=self.param.seed)

        # adding the first generation fo individuals
        for i in range(self.param.pop_init_amount):
            individual = self.param.model(self.num_features)
            self.add_individual(individual)

    # simulates one generation, creates children and adds them to the map
    def sim_generation(self):
        #list of parents
        parents = select_parent(self.param,self.mapE)
        # flag for if rest of parents require mutation (cannot do recombination)
        mutate = False
        # going through all selected parents to create offspring for the generation
        while parents:
            # choosing between mutation or recombination
            if mutate or len(parents) == 1 or random() > self.param.recom_rate:
                p1 = parents.pop(0)
                c1 = p1.mutate_child(self.input_data, self.target_data)
                self.add_individual(c1)
            else:
                p1 = parents.pop(0)
                # if all the remaining parents are the same individual, force mutation for all remaining
                if parents.count(p1) == len(parents):
                    mutate = True
                    c1 = p1.mutate_child(self.input_data, self.target_data)
                    self.add_individual(c1)
                # otherwise, do recombination
                else:
                    p2 = parents.pop(0)

                    # if the two selected parents are the same keep searching for a different parent
                    while p1 == p2:
                        parents.append(p2)
                        p2 = parents.pop(0)

                    c1, c2 = p1.recombine_child(p2, self.input_data, self.target_data)
                    self.add_individual(c1)
                    self.add_individual(c2)
