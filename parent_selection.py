from random import choices

def select_parent(param, mapE):
    if param.parent_selection_method == "random":
        return random_selection(param, mapE)

# random sampling with replacement
def random_selection(param, mapE):
    return choices(list(mapE.values), k = param.generation_amount)
