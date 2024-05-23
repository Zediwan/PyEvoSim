
import unittest
from code.simulation.helper.noise_function import NoiseFunction


class TestWeigh(unittest.TestCase):

    # Calculate weighted average noise with equal weights when none are provided
    def test_weighted_average_with_default_weights(self):
        # Create two NoiseFunction instances
        function1 = NoiseFunction(factor_x=2, factor_y=3, offset_x=1, offset_y=2, pow_x=1, pow_y=2, pow=1.5, fudge=1.2)
        function2 = NoiseFunction(factor_x=1.5, factor_y=2.5, offset_x=-1, offset_y=-2, pow_x=2, pow_y=1, pow=1.2, fudge=1.5)
        x = 1
        y = 1
        result_f1 = function1.noise(x, y)
        result_f2 = function2.noise(x, y)
        expected_result = (result_f1 + result_f2) / 2
        
        result = NoiseFunction.weigh(x, y, [function1, function2])
        # Assert the result is within the expected range
        self.assertEqual(expected_result, result, f"Function noise output does not match. {expected_result} != {result}")