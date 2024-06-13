import unittest
import numpy as np

from lgim.exercise_one import analytical_solution, run_simulation


class CustomAssertions:

    @staticmethod
    def assert_percentage_difference_within_tolerance(test_input: float, baseline: float, tolerance: float):
        percentage_diff = np.abs((test_input - baseline) / baseline) * 100
        if percentage_diff > tolerance:
            print('The percentage difference is larger than the acceptable tolerance level')
            return False
        else:
            return True


class TestExerciseOne(unittest.TestCase, CustomAssertions):

    def setUp(self) -> None:
        self.money = 10
        self.number_of_simulations = 1000000
        self.number_of_flips = 10000
        self.tolerance = 3.0  # In percentage

    def test_simulation(self):
        analytical_loss_prob = analytical_solution(self.money)
        simulation_loss_prob = run_simulation(self.number_of_flips, self.number_of_simulations)
        self.assert_percentage_difference_within_tolerance(simulation_loss_prob, analytical_loss_prob, self.tolerance)


if __name__ == '__main__':
    unittest.main()
