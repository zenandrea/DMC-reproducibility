#! /usr/bin/env python

import os
os.environ["OMP_NUM_THREADS"] = "10"
os.environ["PYSCF_MAX_MEMORY"] = "25000"   # overwrite the default 4000 [MB]

import numpy as np
from numpy import array

import scipy

from pyscf import df, scf, dft
from pyscf import cc, tools

from pyscf import gto as gto_loc

geos = {}

geos['w'] = '''
O 5.000000 7.147077 7.650971
H 4.068066 6.942975 7.563761
H 5.380237 6.896963 6.807984
'''

geos['m'] = '''
C 8.074716 8.896609 8.452975
H 8.154933 9.264317 9.473808
H 8.072329 9.738234 7.763478
H 8.921481 8.249858 8.232870
H 7.150122 8.334028 8.341744
'''

geos['close'] = '''
C 8.074716 8.896609 8.452975
H 8.154933 9.264317 9.473808
H 8.072329 9.738234 7.763478
H 8.921481 8.249858 8.232870
H 7.150122 8.334028 8.341744
O 5.000000 7.147077 7.650971
H 4.068066 6.942975 7.563761
H 5.380237 6.896963 6.807984
'''

geos['far'] = '''
C       15.58354000000001        9.42959800000002        9.70736900000001
H       16.35972400000002       10.13081700000000       10.00665900000000
H       14.66253699999997        9.65943099999998       10.23904000000001
H       15.41394699999998        9.51196199999999        8.63582899999999
H       15.89795200000001        8.41618299999998        9.94794800000000
O        5.00000000000000        6.65576699999999        6.36614799999998
H        5.80708199999998        6.51278800000001        5.87022600000002
H        4.46120600000000        5.88724100000001        6.17422599999999
'''
#del geos['far']
#del geos['close']
#del geos['m']


l_basis = [ f'cc-pCV{i}Z' for i in ['d','t','q','5','6']  ]
l_basis.pop()
l_basis.pop()
l_basis = l_basis[::-1]

res = {}
for basis in l_basis:
    print('* Basis {} *'.format(basis))
    res[basis] = {}
    for syst, geo in geos.items():
        mol = gto_loc.Mole()
        mol.verbose  = 5
        mol.atom     = geo
        mol.basis    = basis
        mol.unit     = 'A'
        # mol.ecp      = 'ccecp'
        mol.charge   = 0
        mol.spin     = 0
        mol.symmetry = True
        mol.output   = f'mol_{basis}_{syst}.output'
        mol.build()

        mf = scf.RHF(mol).density_fit()
        e_scf = mf.kernel()
        print(f'RHF = {e_scf}')

        # Molecular Orbitals
        #mo = mf.mo_coeff

        # CCSD(T) calculation https://pyscf.org/user/cc.html
        mycc = cc.CCSD(mf).run()
        print('CCSD total energy', mycc.e_tot)
        et = mycc.ccsd_t()
        print('CCSD(T) total energy', mycc.e_tot + et)

        res[basis][syst] = {
            'e_hf' : mycc.e_hf ,
            'corr_ccsd' : mycc.e_corr ,
            'corr_t' : et ,
            'e_ccsd' : mycc.e_tot ,
            'e_ccsd(t)' : mycc.e_tot + et }


print(res)

import pickle
#file = open("res.pkl", "w") # "wb" for a binary
#pickle.dump(res, file)

with open('res.pkl', 'wb') as f:
    pickle.dump(res, f)




