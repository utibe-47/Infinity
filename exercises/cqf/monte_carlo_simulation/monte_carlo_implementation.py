import pandas as pd
from pydantic import ValidationError
import matplotlib.pyplot as plt

from exercises.cqf.monte_carlo_simulation.monte_carlo_option_pricing import MonteCarloOptionPricing


def run_option_pricing():
    try:
        option1 = MonteCarloOptionPricing(
            S0=100,
            strike=100,
            rate=0.05,
            sigma=0.2,
            dte=1,
            nsim=100000,
            timesteps=252
        )
    except ValidationError as e:
        print(f"\nValidation error: {e}")
        raise ValueError(f"\nValidation error: {e}")

    paths = pd.DataFrame(option1.simulatepath)
    pseudorandom = option1.pseudorandomnumber
    mean = pseudorandom.mean()
    std = pseudorandom.std()

    call_price = option1.vanillaoption[0]
    put_price = option1.vanillaoption[1]
    plot_vanilla_options(option1, pseudorandom)

    asian_call_price = option1.asianoption[0]
    asian_put_price = option1.asianoption[1]
    up_and_out_barrier_call_price = option1.upandoutcall()[0]
    plot_barrier_options(option1)


def plot_vanilla_options(option, pseudorandom):
    plt.hist(pseudorandom, bins=100)
    plt.plot(option.simulatepath[:, :100])
    plt.xlabel('time steps')
    plt.xlim(0, 252)
    plt.ylabel('index levels')
    plt.title('Monte Carlo Simulated Asset Prices')
    plt.show()


def plot_barrier_options(option):
    figure, axes = plt.subplots(1, 3, figsize=(20, 6), constrained_layout=True)
    title = ['Visualising the Barrier Condition', 'Spot Touched Barrier', 'Spot Below Barrier']

    # Get simulated path
    s = option.simulatepath
    b_shift = option.upandoutcall()[1]

    axes[0].plot(s[:, :200])
    for i in range(200):
        axes[1].plot(s[:, i]) if s[:, i].max() > b_shift else axes[2].plot(s[:, i])

    for i in range(3):
        axes[i].set_title(title[i])
        axes[i].hlines(b_shift, 0, 252, colors='k', linestyles='dashed')

    figure.supxlabel('time steps')
    figure.supylabel('index levels')
    plt.show()


if __name__ == '__main__':
    run_option_pricing()
