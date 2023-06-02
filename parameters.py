from LGP.LGP import LGP

class Parameters:

    def __init__(self):
        self.model = LGP

        #"reg" for MAP_Elites, "CVT" for CVT-MAP_Elites
        self.type = "reg"

        #number of individuals to initialize with
        self.pop_init_amount = 1000

        #number of individuals per generation (number of parents selected)
        self.generation_amount = 1000

        self.parent_selection_method = "random"

        # rates of recombination (inverse rate for mutation)
        self.recom_rate = 0.5

        # matrix of centroids used for CVT-MAP_Elites
        self.centroids = None

        # number of niches for CVT-MAP-elites
        self.num_niches = None

        # seed for random generation things, used for reproducibility
        self.seed = None


