"""
https://scipython.com/book/chapter-8-scipy/examples/finding-the-volume-of-a-torus/
https://mathworld.wolfram.com/Torus.html
https://en.wikipedia.org/wiki/Annulus_(mathematics)
"""
import inspect
from math import pi

r1 = 1.1
r2 = 1.2

def r2D(r):
    return r * 2.0

def disk_area(D):
    return D**2 * pi / 4

def ring_area(disk_area1, disk_area2):
    return abs(disk_area1 - disk_area2)

def cylinder_volume(CSA, length):
    return CSA * length

def D2circum(D):
    return pi * D

def circum2area(circum, D):
    return D /4 * circum




def runifargs(func, callscope):
    def wrapper(*args, **xkwargs):
        nonlocal callscope
        retval = func(*args, **xkwargs)
        callscope["D"] = retval
        print("xkwargs=", xkwargs)
        print("callscope=", callscope)
        return retval
    return wrapper


def runifargs2(func):
    #nonlocal kwargs
    frame = inspect.stack()[1][0]
    callscope = frame.f_locals
    def wrapper(*args, **xkwargs):
        nonlocal callscope
        retval = func(*args, **xkwargs)
        #kwargs["D"] = retval
        print("xkwargs=", xkwargs)
        print("callscope=", callscope)
        return retval
    return wrapper


def cylinder_volume_all(rr, **kwargs):
    op = {}  # kwargs.copy()
    #rr=2.2
    lscope = {**locals(), **kwargs}
    D = runifargs(r2D, lscope)(rr)
    op["D_returned"] = D
    F = runifargs(r2D, lscope)(D)
    op["F_returned"] = F

    G = runifargs2(r2D)(F)
    op["G_returned"] = G
    #print("locals()=", locals())
    print("kwargs=", kwargs)
    return op


def cylinder_volume_all2(**kwargs):
    op = {}
    if "D" not in kwargs:
        try:
            r = kwargs["r"]
            D = r2D(r)
            op["D"] = D
        except Exception as err:
            print(f"ERROR cylinder_volume_all2: failed to run «r2D»: {type(err).__name__} {err}")
            return op
    return op
