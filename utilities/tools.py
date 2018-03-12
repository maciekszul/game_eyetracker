from __future__ import division
import numpy as np
import pandas as pd
import os


def checkEqual(a):
    """
    returns boolean if every element in iterable is equal
    """
    try:
        a = iter(a)
        first = next(a)
        return all(first == rest for rest in a)
    except StopIteration:
        return True


def searchN(a, n):
    """
    search for n repeating numbers
    a = iterable
    n = number of repeating elements
    """
    check = []
    carrier = a[n-1:]
    for index, value in enumerate(carrier):
        check = checkEqual(a[index: index+n])
        if check:
            break
    return check


def pairwise(iterable):
    """
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)


def randomisation(c, n):
    """
    c - conditions dict
    n - number of repetitions
    """
    c = np.tile(c.keys(), n)
    np.random.shuffle(c)
    while searchN(c, 4):
        np.random.shuffle(c)
    return c


def makefolder(path):
    if not os.path.exists(path):
        os.mkdir(path)