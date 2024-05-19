# Define a class for vectors, which are tuples of numbers
class V(tuple):

    # Define a method to add two vectors by adding their corresponding elements
    def __add__(self, other):
        # Use a list comprehension to create a new vector with the added elements
        return V([self[i] + other[i] for i in range(len(self))])  

    # Define a method to subtract two vectors by subtracting their corresponding elements
    def __sub__(self, other):
        # Use a list comprehension to create a new vector with the subtracted elements
        return V([self[i] - other[i] for i in range(len(self))])

    # Define a method to multiply a vector by either a number or another vector
    def __mul__(self, other):
        # Check if the other operand is a number
        if isinstance(other, (int, float)):
            # Use a list comprehension to create a new vector with the scaled elements
            return V([i * other for i in self])
        else: # Assume the other operand is another vector
            # Use a list comprehension and the sum function to calculate the dot product
            return sum([self[i] * other[i] for i in range(len(self))])

    # Define a method to allow multiplication to be done in either order
    def __rmul__(self, other):
        # Just call the __mul__ method with the operands reversed
        return self.__mul__(other)

    # Define a method to divide a vector by either a number or another vector
    def __truediv__(self, other):
        # Check if the other operand is a number
        if isinstance(other, (int, float)):
            # Use a list comprehension to create a new vector with the scaled elements
            return V([i / other for i in self])
        else: # Assume the other operand is another vector
            # Use a list comprehension and the sum function to calculate something like the dot product, but with division instead of multiplication
            return sum([self[i] / other[i] for i in range(len(self))])

    # Define a method to multiply two vectors by multiplying their corresponding elements
    def pmul(self, other):
        # Use a list comprehension to create a new vector with the multiplied elements
        return V([self[i] * other[i] for i in range(len(self))])

    # Define a method to find the cross product of two vectors, which is another vector that is perpendicular to both of them
    def cross(self, other):
        # Check if both vectors have three elements
        if len(self) != 3 or len(other) != 3:
            # Return an error message if not
            return "This vector can't have cross product, it is length " + str(len(self))
        else:
            # Use the formula for the cross product to calculate the components of the new vector
            i = self[1] * other[2] - self[2] * other[1]
            j = self[2] * other[0] - self[0] * other[2]
            k = self[0] * other[1] - self[1] * other[0]
            # Return the new vector as an instance of the class V
            return V((i, j, k))

    # Define a method to get the length of a vector using the Pythagorean theorem
    def __abs__(self):
        # Use the sum function and a list comprehension to calculate the square of the length
        length_squared = sum([i ** 2 for i in self])
        # Use the square root function to get the length
        length = length_squared ** (1/2)
        # Return the length as a number
        return length

    # Define a method to allow subtraction to be done in either order
    def __rsub__(self, other):
        # Just call the __sub__ method with the operands reversed and multiply by -1
        return -1 * self.__sub__(other)

    # Define a method to allow addition to be done in either order
    def __radd__(self, other):
        # Just call the __add__ method with the operands reversed
        return self.__add__(other)

    # Define a method to allow adding using the += operator
    def __iadd__(self, other):
        # Just call the __add__ method and return the result
        return self.__add__(other)

    # Define a method to allow subtracting using the -= operator
    def __isub__(self, other):
        # Just call the __sub__ method and return the result
        return self.__sub__(other)

    # Define a method to convert each element of a vector to an integer
    def intify(self):
        # Use a list comprehension and the int function to create a new vector with the integer elements
        return V([int(i) for i in self])
