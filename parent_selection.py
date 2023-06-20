def select_parent(param, mapE):
    if param.parent_selection_method == "random":
        return random_selection(param, mapE)

# random sampling with replacement
def random_selection(param, mapE):
    return param.rng.choice([x for x in mapE.values() if x], size = 2, replace = False)
