import numba
import numpy as np

"""
The gambling problem can be set out as follows.
The probability of running out of money P(n) can be defined as:

                P(n) = 0.5P(n-1) + 0.5P(n+2)   
                with P(0) = 1
                
or equivalently P(n+2) = 2P(n) - P(n-1)

This is effectively a polynomial with a characteristic equation of 
                x^3 = 2x - 1

Solving the equation, we get roots of 1, 0.5(sqrt(5) - 1), 0.5(-1 - sqrt(5)) thus

                P(n) = a*1^n + b*(alpha-1)^n + c*(-alpha)^n
                where: alpha = 0.5 + sqrt(5)/2 
                a + b + c = 1 as P(0) = 1
       
We know that as the amount of money (n) the gambler starts with increases, the probability of running out of money P(n)
decreases thus as n -> infinity, P(n) -> 0. This means a has to be equal to 0 if not as n -> inf, P(n) cannot tend to 0
Also, as n increases and becomes very large. if c>0 and n is an even number, P(n) > 1. if n is odd, P(n) < 0 and vice 
versa for c<0 therefore c has to be equal to zero.

We can thus simplify the probability of running out of money P(n) as:
                P(n) = (alpha-1)^n where b = 1

Starting with £10, the probability of running out of money is approximately 0.813%
"""


def analytical_solution(money):
    loss_prob = np.power((0.5 + np.sqrt(5)/2 - 1), money) * 100
    return loss_prob


@numba.njit
def gambling_simulator(num_flips: int, num_simulations: int) -> np.ndarray:
    money_array = np.zeros(num_simulations, dtype=float)

    for j in range(num_simulations):
        tosses = np.random.randint(0, 2, size=num_flips)
        money = 10
        for i in range(num_flips):
            toss = tosses[i]
            if toss == 1:
                money += 2.0
            else:
                money -= 1.0
            if money <= 0.0:
                break
        money_array[j] = money
        tosses = None
    return money_array


def run_simulation(number_of_flips: int, number_of_simulations: int) -> float:
    money_held = gambling_simulator(number_of_flips, number_of_simulations)
    total_loss_count = len(np.where(money_held <= 0.0)[0])
    prob_total_loss = total_loss_count/number_of_simulations * 100
    return prob_total_loss


if __name__ == '__main__':
    _money = 10
    num_sims = 1000000
    _num_flips = 10000
    analytical_loss = analytical_solution(_money)
    sim_loss = run_simulation(_num_flips, num_sims)
    print('The analytical loss probability is {}%'.format(analytical_loss))
    print('The simulated loss probability is {}%'.format(sim_loss))
