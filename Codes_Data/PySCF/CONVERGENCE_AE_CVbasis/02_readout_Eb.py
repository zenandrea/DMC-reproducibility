#! /usr/bin/env python

import numpy as np
from numpy import array
import pandas as pd
import scipy
import pickle
import re

#with open('res.pkl', 'rb') as f:
#	res = pickle.load(f)

res = {}
#l_basis = [ f'cc-pCV{i}Z' for i in ['d','t','q','5','6']  ]
l_basis = [ f'cc-pCV{i}Z' for i in ['d','t','q']  ]
l_basis = l_basis[::-1]

for basis in l_basis:
    res[basis] = {}
    for syst in ['w','m','close','w_cp','m_cp']:
        with open( f'mol_{basis}_{syst}.output', 'r' ) as f:
            for l in f.readlines():
                if re.search( 'converged SCF energy', l ):
                    e_hf = float( l.split()[-1] )
                if re.search( 'E\(RCCSD\)', l ):
                    ll = l.split()
                    e_corr = float( ll[-1] )
                    e_ccsd = float( ll[2] )
                if re.search( 'CCSD\(T\) correction' , l ):
                    e_t = float( l.split()[-1] )
        res[basis][syst] = {
            'e_hf' : e_hf ,
            'corr_ccsd' : e_corr ,
            'corr_t' : e_t ,
            'e_ccsd' : e_ccsd ,
            'e_ccsd(t)' : e_ccsd + e_t }


res_hf = {}
res_corr_ccsd = {}
res_corr_t = {}

for b,r in res.items():
    res_hf[b] = {}
    res_corr_ccsd[b] = {}
    res_corr_t[b] = {}
    for syst,data in r.items():
        res_hf[b][syst] = data['e_hf']
        res_corr_ccsd[b][syst] = data['corr_ccsd']
        res_corr_t[b][syst] = data['corr_t']

df = {}
df['hf'] = pd.DataFrame(res_hf).T
df['c_ccsd'] = pd.DataFrame(res_corr_ccsd).T
df['c_t'] = pd.DataFrame(res_corr_t).T
df['ccsd(t)'] = df['hf']+df['c_ccsd']+df['c_t']

for method, d in df.items():
    d['Eb'] = d.close - d.w - d.m
    d['Eb_cp'] = d.close - d.w_cp - d.m_cp
    #d['SCerr'] = d.far - d.w - d.m
    d.to_csv( f'res_{method}.csv' )

c = 1.0e3 * 27.21138505   # H to meV

#for method, d in df.items():
#    print( method )
#    print( d.Eb * c )

methods = df.keys()
Eb = pd.DataFrame( [ df[i].Eb for i in methods ], index=methods ).T
Eb = Eb * c   # Eb in meV
Eb['ccsd']    = Eb.hf + Eb.c_ccsd
Eb['ccsd(t)'] = Eb.hf + Eb.c_ccsd + Eb.c_t

Eb.to_csv( 'res_Eb.csv' )
print('Interaction energy Eb/meV')
print(Eb)

Eb_cp = pd.DataFrame( [ df[i].Eb_cp for i in methods ], index=methods ).T
Eb_cp = Eb_cp * c   # Eb in meV
Eb_cp['ccsd']    = Eb_cp.hf + Eb_cp.c_ccsd
Eb_cp['ccsd(t)'] = Eb_cp.hf + Eb_cp.c_ccsd + Eb_cp.c_t

Eb_cp.to_csv( 'res_Eb_cp.csv' )
print('Interaction energy Eb_cp/meV using counterpoise correction')
print(Eb_cp)


#       res[basis][syst] = {
#           'e_hf' : mycc.e_hf ,
#           'corr_ccsd' : mycc.e_corr ,
#           'corr_t' : et ,
#           'e_ccsd' : mycc.e_tot ,
#           'e_ccsd(t)' : mycc.e_tot + et }





