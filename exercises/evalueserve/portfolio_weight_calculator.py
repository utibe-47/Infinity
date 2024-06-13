
def calculate_weight(units):
    weights = units.div(units.sum(axis=1), axis=0)
    return weights
