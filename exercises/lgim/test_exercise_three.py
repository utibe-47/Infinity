import unittest
import random

from lgim.exercise_three import find_increasing_sub_list, generate_word_list, find_ascending_sublist_numpy


class TestExerciseThree(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_numpy_implementation(self):
        _words = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve']
        expected_output = ['two', 'three']
        output = find_ascending_sublist_numpy(_words)
        self.assertEqual(expected_output, output)

    def test_base_implementation(self):
        _words = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve']
        expected_output = ['two', 'three']
        output = find_increasing_sub_list(_words)
        self.assertEqual(expected_output, output)

    def test_base_and_numpy_case(self):
        for _ in range(10000):
            ranges = random.sample(range(1, 99), 2)
            ranges.sort()
            low, high = ranges
            _numbers = list(range(low, high + 1))
            words = generate_word_list(_numbers)
            result = find_increasing_sub_list(words)
            output = find_ascending_sublist_numpy(words)
            self.assertEqual(result, output)


if __name__ == '__main__':
    unittest.main()
