class Parameters:

    def __init__(self, input_data, target_data, num_samples, rng, model, model_param):
        self.input_data = input_data
        self.target_data = target_data
        self.num_samples = num_samples

        self.model = model

        self.model_param = model_param

        #"reg" for MAP_Elites, "CVT" for CVT-MAP_Elites
        self.type = "CVT"

        #number of individuals to initialize with
        self.pop_init_amount = 1000

        #number of individuals per generation (number of parents selected)
        self.generation_amount = 1000

        self.parent_selection_method = "random"

        # lexicase or fitness
        self.comparison_method = 'lexicase'

        # rates of recombination (inverse rate for mutation)
        self.recom_rate = 0.9

        self.mut_rate = 1

        # number of niches for CVT-MAP-elites
        self.num_niches = None

        # seed for random generation things, used for reproducibility
        self.rng = rng


