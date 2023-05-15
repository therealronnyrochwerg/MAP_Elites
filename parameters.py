from LGP.LGP import LGP

class Parameters:

    def __init__(self):
        self.model = LGP

        #"reg" for MAP-Elites, "CVT" for CVT-MAP-Elites
        self.type = "reg"

        #number of individuals to initialize with
        self.pop_init_amount = 1000

        #number of individuals per generation
        self.generation_amount = 1000

        self.parent_selection_method = "random"

