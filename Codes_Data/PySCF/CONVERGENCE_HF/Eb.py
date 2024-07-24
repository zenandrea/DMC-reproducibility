#! /usr/bin/env python

import numpy as np
from numpy import array
import pandas as pd
import scipy
import pickle

with open('res.pkl', 'rb') as f:
	res = pickle.load(f)

res

res_hf = {}

for b,r in res.items():
    res_hf[b] = {}
    for syst,data in r.items():
        res_hf[b][syst] = data['e_hf']

df = {}
df['hf'] = pd.DataFrame(res_hf).T

for method, d in df.items():
    d['Eb'] = d.close - d.w - d.m

c = 1.0e3 * 27.21138505   # H to meV

#for method, d in df.items():
#    print( method )
#    print( d.Eb * c )

methods = df.keys()
Eb = pd.DataFrame( [ df[i].Eb for i in methods ], index=methods ).T
Eb = Eb * c   # Eb in meV

print(Eb)


#       res[basis][syst] = {
#           'e_hf' : mycc.e_hf ,
#           'corr_ccsd' : mycc.e_corr ,
#           'corr_t' : et ,
#           'e_ccsd' : mycc.e_tot ,
#           'e_ccsd(t)' : mycc.e_tot + et }





