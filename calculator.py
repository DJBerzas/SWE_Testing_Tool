class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def power(self, base, exp):
        if exp < 0:
            raise ValueError("Negative exponents not supported")
        return base ** exp
    
    def mod(self, a, b):
        if b <= 0:
            raise ValueError("Modulo by non-positive number")
        return a % b
    
    def floor_divide(self, a, b):
        if b != 0:
            return a // b
        raise ValueError("Cannot divide by zero")
    
    def abs(self, x):
        if x >= 0:
            return x
        return -x
    
    def max(self, a, b):
        if a > b:
            return a
        return b
    
    def min(self, a, b):
        if a < b:
            return a
        return b 