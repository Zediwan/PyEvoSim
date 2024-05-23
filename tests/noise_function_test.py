
import unittest
from code.simulation.helper.noise_function import NoiseFunction


class TestWeigh(unittest.TestCase):
    def test_weigh_without_weights(self):
        """
        Tests if NoiseFunction.weigh works correctly if no weights are given
        """
        function1 = NoiseFunction(factor_x=2, factor_y=3, offset_x=1, offset_y=2, pow_x=1, pow_y=2, pow=1.5, fudge=1.2)
        function2 = NoiseFunction(factor_x=1.5, factor_y=2.5, offset_x=-1, offset_y=-2, pow_x=2, pow_y=1, pow=1.2, fudge=1.5)
        x = 1
        y = 1
        result_f1 = function1.noise(x, y)
        result_f2 = function2.noise(x, y)
        expected_result = (result_f1 + result_f2) / 2
        
        result = NoiseFunction.weigh(x, y, [function1, function2])

        self.assertEqual(expected_result, result, "Function noise output does not match.")

    def test_weigh_with_custom_weights(self):
        """
        Tests if NoiseFunction.weigh works correctly if custom weights for each function are given.
        """
        function1 = NoiseFunction(factor_x=2, factor_y=3, offset_x=1, offset_y=2, pow_x=1, pow_y=2, pow=1.5, fudge=1.2)
        function2 = NoiseFunction(factor_x=1.5, factor_y=2.5, offset_x=-1, offset_y=-2, pow_x=2, pow_y=1, pow=1.2, fudge=1.5)

        weigth_f1 = 1
        weigth_f2 = 2

        x = 1
        y = 1
        result_f1 = function1.noise(x, y) * weigth_f1
        result_f2 = function2.noise(x, y) * weigth_f2
        expected_result = (result_f1 + result_f2) / (weigth_f1 + weigth_f2)

        result = NoiseFunction.weigh(x, y, [function1, function2], [weigth_f1, weigth_f2])

        self.assertEqual(expected_result, result, "Function noise output does not match.")

    def test_weigh_with_insufficient_weights(self):
        """
        Tests if NoiseFunction.weigh works correctly if fewer weights than functions are given
        """
        function1 = NoiseFunction(factor_x=2, factor_y=3, offset_x=1, offset_y=2, pow_x=1, pow_y=2, pow=1.5, fudge=1.2)
        function2 = NoiseFunction(factor_x=1.5, factor_y=2.5, offset_x=-1, offset_y=-2, pow_x=2, pow_y=1, pow=1.2, fudge=1.5)

        weigth_f1 = 2
        expected_weight_f2 = 1

        x = 1
        y = 1
        result_f1 = function1.noise(x, y) * weigth_f1
        result_f2 = function2.noise(x, y) * expected_weight_f2
        expected_result = (result_f1 + result_f2) / (weigth_f1 + expected_weight_f2)

        result = NoiseFunction.weigh(x, y, [function1, function2], [weigth_f1])

        self.assertEqual(expected_result, result, "Function noise output does not match.")

    def test_weigh_without_functions(self):
        """
        Tests if NoiseFunction.weigh raises an error correctly if list of functions given is empty
        """
        x = 1
        y = 1
        try:
            NoiseFunction.weigh(x, y, [])
        except ValueError:
            pass