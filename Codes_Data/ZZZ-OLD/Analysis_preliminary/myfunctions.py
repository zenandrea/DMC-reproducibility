import numpy as np
import glob
import os
import re
import pandas as pd
import pyblock


def EneDiff(a,b,c=627.503):
    return (a-b)*c


def EneDiffErr(a,b,c=627.503):
    return c*(( a**2 + b**2 )**0.5)


def EneDiffX(a,b,c=627.503):
    return (a.ene-b.ene)*c, c*(( a.err**2 + b.err**2 )**0.5)


def EneDiff_AA(aa,a,c=627.503):
    ene = c*( aa.ene - 2*a.ene )
    err = c*(( aa.err**2 + 4* a.err**2 )**0.5 )
    return ene, err

def x_axis( df, code ):
    x = np.array( df.index )
    if code.startswith('TurboRVB'):
        xnew = x**2
    elif code.startswith('QMC=Chem'):
        xnew = x #* 20
    else:
        xnew = x
    return xnew
