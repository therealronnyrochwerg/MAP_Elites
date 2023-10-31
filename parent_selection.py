import numpy as np


def select_parent(param, mapE):
    if param.parent_selection_method == "random":
        return random_selection(param, mapE)

# random sampling with replacement
def random_selection(param, mapE):
    return param.rng.choice([x for x in mapE.values() if x], size = 2, replace = False)

def lexicase(pop, samples, target, num_return = 1):
    predictions = []
    for i, individual in enumerate(pop):
        prediction = individual.predict(samples)
        predictions.append([target - prediction,i])

    for i in range(len(samples)):
        min_err = min(predictions, key=lambda x: abs(x[0][i]))[0][i]
        if not np.isnan(min_err):
            predictions = [x for x in predictions if x[0][i] <= min_err]
        else:
            predictions = [x for x in predictions if not np.isnan(x[0][i])]
        if len(predictions) == 0:
            return None
        elif len(predictions) == num_return:
            return pop[predictions[0][1]]
    return pop[predictions[0][1]]

