from .parent_selection import select_parent
from .centroids import create_centroids, closest_centroid, shift_centroid, compare_ind
import numpy as np

class MAPElites (object):

    # model is a reference to a class for the model (like LGP)
    def __init__(self, param):
        self.param = param
        # matrix of centroids used for CVT-MAP_Elites
        self.gen_centroids = None
        self.cur_centroids = None
        if self.param.type == 'CVT':
            self.niche_popularity = [0] * self.param.num_niches

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
            chosen_centroid = closest_centroid(self.gen_centroids, individual.behavior)
            self.niche_popularity[chosen_centroid] += 1
            # if there is already an individual in the niche
            if self.mapE[chosen_centroid]:
                # if the new individual has higher fitness
                chosen_ind = compare_ind(self.param, [individual, self.mapE[chosen_centroid]], self.gen_centroids[chosen_centroid])
                if chosen_ind is not None:
                # replace the old individual and shift the centroid according the new behavior
                    self.mapE[chosen_centroid] = chosen_ind
                    self.cur_centroids[chosen_centroid] = shift_centroid(self.cur_centroids[chosen_centroid], individual.behavior)
            else:
                # if there is no individual, add and shift
                self.mapE[chosen_centroid] = individual
                self.cur_centroids[chosen_centroid] = shift_centroid(self.cur_centroids[chosen_centroid],
                                                                       individual.behavior)
        else:
            quit("incompatible type in parameters")

    # used for initialization (gen 0)
    def initialize_centroids(self):
        # if type is CVT have to initialize the centroids
        if self.param.type == "CVT":
            self.mapE = dict.fromkeys(range(self.param.num_niches))
            self.gen_centroids = create_centroids(self.param.num_samples, self.param.num_niches, self.param.rng)
            self.cur_centroids = np.copy(self.gen_centroids)


    def initialize_population(self):
        # adding the first generation fo individuals
        for i in range(self.param.pop_init_amount):
            individual = self.param.model(self.param.model_param)
            individual.initialize(self.param.input_data, self.param.target_data, name = i)
            self.add_individual(individual)

        self.gen_centroids = np.copy(self.cur_centroids)

    # simulates one generation, creates children and adds them to the map
    def sim_generation(self):
        for i in range(self.param.generation_amount//2):
            #list of parents
            parents = select_parent(self.param, self.mapE)
            child1 = parents[0].make_copy()
            child2 = parents[1].make_copy()
            if self.param.rng.random() < self.param.recom_rate:
                child1.recombine(child2)
            elif self.param.rng.random() < self.param.mut_rate:
                child1.mutate()
                child2.mutate()

            child1.evaluate(self.param.input_data, self.param.target_data)
            child2.evaluate(self.param.input_data, self.param.target_data)
            self.add_individual(child1)
            self.add_individual(child2)
        self.gen_centroids = np.copy(self.cur_centroids)

    def print_map(self):
        for behaviour, model in self.mapE.items():
            if model:
                print(behaviour, model.fitness)
            else:
                print(behaviour, None)