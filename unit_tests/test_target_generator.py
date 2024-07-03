from unittest import TestCase

from target_generator.target_generator import TargetGenerator
from target_generator.target_generator_helpers import get_allocations, get_signals, read_prices, get_aum


class TestTargetGenerator(TestCase):

    def setUp(self):
        self.target_generator = TargetGenerator()
        self.allocations = get_allocations()
        self.signals = get_signals()
        self.prices = read_prices()
        self.target_generator.aum = get_aum()

    def test_target_generator_runner(self):
        targets = self.target_generator.run(self.signals, self.allocations, self.prices)
        self.assertIsNotNone(targets)
