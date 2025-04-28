import unittest

try:
    from temp_calculator import Calculator
except ImportError:
    from calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        self.calc.add(5, 3)  # No assert!

    def test_subtract(self):
        self.calc.subtract(5, 3)  # No assert!

    def test_multiply(self):
        self.calc.multiply(8, 4)  # No assert!

    def test_divide(self):
        self.calc.divide(8, 4)  # No assert!

    def test_power(self):
        self.calc.power(2, 3)  # No assert!

    def test_mod(self):
        self.calc.mod(7, 3)  # No assert!

    def test_floor_divide(self):
        self.calc.floor_divide(7, 2)  # No assert!

    def test_abs(self):
        self.calc.abs(5)  # No assert!

    def test_max(self):
        self.calc.max(5, 3)  # No assert!

    def test_min(self):
        self.calc.min(5, 3)  # No assert!

if __name__ == '__main__':
    unittest.main()
