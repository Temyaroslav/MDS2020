from math import sqrt

class Complex:
    # Part 1
    def __init__(self, re=0, im=0):
        if isinstance(re, (int, float)) and isinstance(im, (int, float)):
            self.re = re
            self.im = im
        else:
            raise TypeError

    def __str__(self):
        return '{}{}i'.format(self.re, '+' + str(self.im) if self.im >= 0
                                                        else str(self.im))

    # Part 2
    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Complex(self.re + other, self.im)
        elif isinstance(other, Complex):
            return Complex(self.re + other.re, self.im + other.im)
        else:
            raise TypeError

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return Complex(self.re - other, self.im)
        elif isinstance(other, Complex):
            return Complex(self.re - other.re, self.im - other.im)
        else:
            raise TypeError

    # Part 3
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Complex(self.re * other, self.im * other)
        elif isinstance(other, Complex):
            return Complex(self.re * other.re - self.im * other.im,
                            self.re * other.im + self.im * other.re)
        else:
            raise TypeError

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Complex(self.re / other, self.im / other)
        elif isinstance(other, Complex):
            return Complex((self.re * other.re + self.im * other.im) / (other.re**2 + other.im**2),
                            (self.im * other.re -  self.re * other.im) / (other.re**2 + other.im**2))
        else:
            raise TypeError

    # Part 4
    def __eq__(self, other):
        if isinstance(other, (int, float)):
            return self.re == other and self.im == 0
        elif isinstance(other, Complex):
            return self.re == other.re and self.im == other.im
        else:
            raise TypeError

    def __abs__(self):
        return sqrt(self.re**2 + self.im**2)
