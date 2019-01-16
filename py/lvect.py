""" Lorentz vector class """

import numpy as np

class Vect(object):
    """ Three-vector """
    def __init__(self, x, y, z):
        self.data = np.array([x, y, z])

    def __abs__(self):
        """ Absolute value """
        return np.sqrt(self.abs2())

    def __add__(self, y):
        """ Operator + """
        return Vect(*(self.data + y.data))

    def __sub__(self, y):
        """ Operator - """
        return Vect(*(self.data - y.data))

    def __neg__(self):
        """ Operator - """
        return Vect(*(self.data * -1))

    def __pos__(self):
        """ Operator - """
        return self

    def __mul__(self, a):
        """ Operator + """
        return Vect(*(self.data * a))
    
    def __div__(self, a):
        """ Operator + """
        return Vect(*(self.data / a))

    # def __iter__(self):
    #     assert((i >=0) and (i < 3))
    #     return self.data[i]

    def dot(self, y):
        return np.dot(self.data, y.data)

    def abs2(self):
        """ Absolute value squared """
        return np.sum(self.data**2)

    def pt(self):
        """ Perp mom """
        return np.sum(self.data[:-1]**2)

    def costh(self):
        """ Cosine of polar angle """
        return self.data[-1] / abs(self)

class LVect(object):
    """ Lorentz vector """
    def __init__(self, t, x, y=None, z=None):
        self.t = t
        self.r = x if y is None else Vect(x, y, z)

    def __abs__(self):
        """ Absolute value """
        return np.sqrt(self.m2())

    def __add__(self, y):
        """ Operator + """
        return LVect(self.t + y.t, self.r.data + y.r.data)

    def __mul__(self, a):
        """ Operator + """
        return LVect(self.t * a, self.r.data * a)
    
    def __div__(self, a):
        """ Operator + """
        return LVect(self.t / a, self.r.data / a)

    def __sub__(self, y):
        """ Operator - """
        return LVect(self.t - y.t, self.r.data - y.r.data)

    def __neg__(self):
        """ Operator - """
        return LVect(-self.t, self.r.data * -1)

    def __pos__(self):
        """ Operator - """
        return self

    def m2(self):
        """ Norm of Lorentz vector """
        return self.t**2 - self.r.abs2()

    def boost(self, v):
        """ Lorentz boost """
        beta = abs(v)
        gamma = 1./ np.sqrt(1 - beta**2)
        direction  = -v / beta
        dot = self.r.dot(direction)
        return LVect(gamma * (self.t - beta * dot),
                     self.r + direction * ((gamma - 1) * dot - gamma * self.t * beta))
