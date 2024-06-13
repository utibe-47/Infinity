import pandas as pd


def initialise_basket_params(equity_notional, initial_basket_value):
    basket_unit = []
    basket_value = []
    initial_basket_unit = equity_notional/initial_basket_value
    basket_unit.append(initial_basket_unit)
    basket_value.append(initial_basket_value)
    return basket_unit, basket_value


def calculate_basket_value(previous_basket_value, price, previous_price, previous_units):
    basket_value = previous_basket_value * ((previous_units.mul(price)).sum(axis=1)[0]/previous_units.mul(previous_price).sum(axis=1)[0])
    return basket_value


def calculate_basket_units(basket_value, previous_basket_unit, current_units, previous_units, price):
    basket_unit = previous_basket_unit + ((current_units - previous_units).mul(price).sum(axis=1))[0]/basket_value
    return basket_unit


def calculate_prime_units(current_units, basket_unit):
    prime_units = current_units/basket_unit
    return prime_units


def calculate_value(prices, units, equity_notional, initial_basket_value):
    rebalance_count = 0
    prime_units = []
    basket_units, basket_values = initialise_basket_params(equity_notional, initial_basket_value)
    for count, (index, row) in enumerate(prices.iterrows()):
        if count == 0:
            initial_units = units.iloc[[0]].reset_index(drop=True)
            initial_prime_units = calculate_prime_units(initial_units, basket_units[0])
            prime_units.append(initial_prime_units)
            continue
        previous_basket_value = basket_values[count-1]
        previous_price = prices.iloc[[count-1]].reset_index(drop=True)
        price = prices.iloc[[count]].reset_index(drop=True)
        if rebalance_count + 1 < units.shape[0] and index >= units.index[rebalance_count+1]:
            rebalance_count += 1
        current_units = units.iloc[[rebalance_count]].reset_index(drop=True)
        if rebalance_count > 0:
            previous_unit_index = rebalance_count - 1
        else:
            previous_unit_index = rebalance_count
        previous_units = units.iloc[[previous_unit_index]].reset_index(drop=True)
        previous_basket_unit = basket_units[count-1]

        basket_value = calculate_basket_value(previous_basket_value, price, previous_price, previous_units)
        basket_unit = calculate_basket_units(basket_value, previous_basket_unit, current_units, previous_units, price)
        prime_unit = calculate_prime_units(current_units, basket_unit)

        basket_values.append(basket_value)
        basket_units.append(basket_unit)
        prime_units.append(prime_unit)

    prime_units = pd.concat(prime_units)
    return basket_values, basket_units, prime_units
