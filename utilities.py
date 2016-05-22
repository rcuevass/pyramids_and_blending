import math as mt

"""
This module contains various functions that support basic operations within 
laplace_pyramid and gauss_pyramid modules
"""


def incrDim(n):
    """
    Function that determines the size of extended vector resutlting from convoluting it with kernel w
    n: length of vector
    return: new extended length
    """
    n_ = int(mt.floor(mt.log(n,2)))
    return 2**(n_+1) if n%2 == 0 else (2**(n_+1)) + 1

def redDim(n):
    """
    Function that determines the size of reduced vector resutlting from convoluting it with kernel w
    n: length of vector
    return: new reduced length
    """
    n_ = int(mt.floor(mt.log(n,2)))
    return 2**(n_-1) if n%2 == 0 else (2**(n_-1)) + 1