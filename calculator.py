class Calculator:
    def add(self, a, b):
        # Issue 1: Potential integer overflow not handled
        return a + b
    
    def subtract(self, a, b):
        # Issue 2: No handling of negative results
        return a - b
    
    def multiply(self, a, b):
        # Issue 3: No handling of large numbers
        return a * b
    
    def divide(self, a, b):
        # Issue 4: Only checks for zero, not for very small numbers
        if b == 0:  # This will be mutated to b != 0
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def power(self, base, exp):
        # Issue 5: No validation of input types
        # Issue 6: No handling of negative exponents
        if exp < 0:  # Mutation: < to >
            raise ValueError("Negative exponents not supported")
        return base ** exp
    
    def mod(self, a, b):
        if b <= 0:  # Mutation: <= to >=
            raise ValueError("Modulo by non-positive number")
        return a % b
    
    def floor_divide(self, a, b):
        if b != 0:  # Mutation: != to ==
            return a // b
        raise ValueError("Cannot divide by zero")
    
    def abs(self, x):
        if x >= 0:  # Mutation: >= to <=
            return x
        return -x
    
    def max(self, a, b):
        if a > b:  # Mutation: > to <
            return a
        return b
    
    def min(self, a, b):
        if a < b:  # Mutation: < to >
            return a
        return b 