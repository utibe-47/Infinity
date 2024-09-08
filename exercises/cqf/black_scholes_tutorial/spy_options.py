from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from black_scholes_model import BlackScholesModel, OptionInputs


def create_option(dte, rate, spot, strike, vol):
    spy_opt = BlackScholesModel(
        inputs=OptionInputs(option_type="call", spot_price=spot, strike_price=strike, time_to_expiry=dte,
                            risk_free_rate=rate, volatility=vol))
    print(f'Option Price of SPY240930C00533000 with BS Model is {spy_opt.price:0.4f}')
    return spy_opt


def calculate_greeks(dte, options, rate, spot):
    # Filter calls for strike at or above 530
    df = options.calls[(options.calls['strike'] >= 530) & (options.calls['strike'] <= 550)]
    df.reset_index(drop=True, inplace=True)
    df = pd.DataFrame({'Strike': df['strike'],
                       'Price': df['lastPrice'],
                       'ImpVol': df['impliedVolatility']})

    df['Delta'] = df['Gamma'] = df['Vega'] = df['Theta'] = 0.
    for i in range(len(df)):
        option = BlackScholesModel(
            inputs=OptionInputs(option_type="call", spot_price=spot, strike_price=df['Strike'].iloc[i],
                                time_to_expiry=dte, risk_free_rate=rate, volatility=df['ImpVol'].iloc[i]))

        df['Delta'].iloc[i] = option.delta
        df['Gamma'].iloc[i] = option.gamma
        df['Vega'].iloc[i] = option.vega
        df['Theta'].iloc[i] = option.theta

    return df


def visualize_greeks(option_data_df):
    fig, ax = plt.subplots(2, 2, figsize=(20, 10))
    ax[0, 0].plot(option_data_df['Strike'], option_data_df['Delta'], color='r', label='SEP 24')
    ax[0, 1].plot(option_data_df['Strike'], option_data_df['Gamma'], color='b', label='SEP 24')
    ax[1, 0].plot(option_data_df['Strike'], option_data_df['Vega'], color='k', label='SEP 24')
    ax[1, 1].plot(option_data_df['Strike'], option_data_df['Theta'], color='g', label='SEP 24')
    ax[0, 0].set_title('Delta'), ax[0, 1].set_title('Gamma'), ax[1, 0].set_title('Vega'), ax[1, 1].set_title('Theta')
    ax[0, 0].legend(), ax[0, 1].legend(), ax[1, 0].legend(), ax[1, 1].legend()
    fig.suptitle('Greeks Vs Strike')
    plt.show()


def run():
    spy = yf.Ticker('SPY')
    options = spy.option_chain('2024-09-30')

    dte = (datetime(2024, 9, 30) - datetime.today()).days / 365
    spot = 532.905
    strike = 533
    rate = 0.0
    vol = 0.2107

    spy_opt = create_option(dte, rate, spot, strike, vol)
    print(f'Option Price of SPY240930C00533000 with BS Model is {spy_opt.price:0.4f}')

    option_data_df = calculate_greeks(dte, options, rate, spot)
    visualize_greeks(option_data_df)


if __name__ == '__main__':
    run()
