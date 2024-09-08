import opstrat as op
from tabulate import tabulate

from black_scholes_model import BlackScholesModel, OptionInputs


def run():
    call_option_inputs = OptionInputs(
        option_type="call",
        spot_price=100,
        strike_price=100,
        time_to_expiry=1,
        risk_free_rate=0.05,
        volatility=0.2
    )
    call_option, put_option = price_options(call_option_inputs)
    visualize_options(call_option_inputs, call_option)


def price_options(call_option_inputs):

    # Create a copy of the inputs with the option_type set to "put"
    put_option_inputs = call_option_inputs.model_copy(update={"option_type": "put"})

    # Create a BlackScholesModel object with the inputs
    call_option = BlackScholesModel(inputs=call_option_inputs)
    put_option = BlackScholesModel(inputs=put_option_inputs)

    header = ['Option Type', 'Option Price', 'Delta', 'Gamma', 'Theta', 'Vega', 'Rho']
    table = [
        [call_option_inputs.option_type, call_option.price, call_option.delta, call_option.gamma, call_option.theta,
         call_option.vega, call_option.rho],
        [put_option_inputs.option_type, put_option.price, put_option.delta, put_option.gamma, put_option.theta,
         put_option.vega, put_option.rho]]

    print(tabulate(table, header))
    return call_option, put_option


def visualize_options(call_option_inputs, call_option):
    # Single Plotter
    op.single_plotter(spot=call_option_inputs.spot_price, strike=call_option_inputs.strike_price, op_type='c',
                      tr_type='b', op_pr=call_option.price, spot_range=25)

    # Short Straddle
    leg1 = BlackScholesModel(
        inputs=OptionInputs(option_type="call", spot_price=100, strike_price=100, time_to_expiry=1, risk_free_rate=0.05,
                            volatility=0.2))
    leg2 = BlackScholesModel(
        inputs=OptionInputs(option_type="put", spot_price=100, strike_price=100, time_to_expiry=1, risk_free_rate=0.05,
                            volatility=0.2))

    op_list = define_option_parameters(leg1, leg2)

    op.multi_plotter(spot=leg1.inputs.spot_price, spot_range=25, op_list=op_list)

    # Strangle
    str_leg1 = BlackScholesModel(
        inputs=OptionInputs(option_type="call", spot_price=100, strike_price=110, time_to_expiry=1, risk_free_rate=0.05,
                            volatility=0.2))
    str_leg2 = BlackScholesModel(
        inputs=OptionInputs(option_type="put", spot_price=100, strike_price=90, time_to_expiry=1, risk_free_rate=0.05,
                            volatility=0.2))

    op_list = define_option_parameters(str_leg1, str_leg2)
    op.multi_plotter(spot=leg1.inputs.spot_price, spot_range=25, op_list=op_list)

    # Iron condor
    leg1 = BlackScholesModel(
        inputs=OptionInputs(option_type="call", spot_price=100, strike_price=100, time_to_expiry=1, risk_free_rate=0.05,
                            volatility=0.2))
    leg2 = BlackScholesModel(
        inputs=OptionInputs(option_type="call", spot_price=100, strike_price=105, time_to_expiry=1, risk_free_rate=0.05,
                            volatility=0.2))
    leg3 = BlackScholesModel(
        inputs=OptionInputs(option_type="put", spot_price=100, strike_price=95, time_to_expiry=1, risk_free_rate=0.05,
                            volatility=0.2))
    leg4 = BlackScholesModel(
        inputs=OptionInputs(option_type="put", spot_price=100, strike_price=90, time_to_expiry=1, risk_free_rate=0.05,
                            volatility=0.2))

    op_1 = {'op_type': 'c', 'strike': leg1.inputs.strike_price, 'tr_type': 's', 'op_pr': leg1.price}
    op_2 = {'op_type': 'c', 'strike': leg2.inputs.strike_price, 'tr_type': 'b', 'op_pr': leg2.price}
    op_3 = {'op_type': 'p', 'strike': leg3.inputs.strike_price, 'tr_type': 's', 'op_pr': leg3.price}
    op_4 = {'op_type': 'p', 'strike': leg4.inputs.strike_price, 'tr_type': 'b', 'op_pr': leg4.price}

    op_list = [op_1, op_2, op_3, op_4]
    op.multi_plotter(spot=leg1.inputs.spot_price, spot_range=25, op_list=op_list)


def define_option_parameters(leg1, leg2):
    op_1 = {'op_type': 'c', 'strike': leg1.inputs.strike_price, 'tr_type': 's', 'op_pr': leg1.price}
    op_2 = {'op_type': 'p', 'strike': leg2.inputs.strike_price, 'tr_type': 's', 'op_pr': leg2.price}
    op_list = [op_1, op_2]
    return op_list


if __name__ == '__main__':
    run()
