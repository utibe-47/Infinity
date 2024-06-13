import unittest
import numpy as np

from lgim.exercise_two import battleship_counter


class TestExerciseTwo(unittest.TestCase):

    def setUp(self) -> None:
        self.expected_number_of_ships = [5, 6, 2]
        self.input_matrices = [np.array([[0.0, 0.31, 0.0, 0.77], [0.0, 0.0, 0.0, 0.0], [0.69, 0.0, 0.86, 0.0],
                                         [0.0, 0.0, 0.0, 0.36]]),
                               np.array([[0.66, 0.0, 0.0, 0.17], [0.0, 0.0, 0.52, 0.0], [0.00, 0.86, 0.0, 0.11],
                                         [0.58, 0.0, 0.0, 0.36]]),
                               np.array([[0.0, 0.0, 0.0, 0.0], [0.89, 0.21, 0.50, 0.0], [0.11, 0.0, 0.0, 0.30],
                                         [0.0, 0.0, 0.0, 0.36]])]

    def test_battleship_counter(self):
        for count, input_matrix in enumerate(self.input_matrices):
            expected_ships = self.expected_number_of_ships[count]
            actual_number_of_ships = battleship_counter(input_matrix)
            self.assertEqual(expected_ships, actual_number_of_ships)


if __name__ == '__main__':
    unittest.main()
