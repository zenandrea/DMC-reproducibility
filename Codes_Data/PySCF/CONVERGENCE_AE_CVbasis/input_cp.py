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

geos['w_cp'] = '''
X-C 8.074716 8.896609 8.452975
X-H 8.154933 9.264317 9.473808
X-H 8.072329 9.738234 7.763478
X-H 8.921481 8.249858 8.232870
X-H 7.150122 8.334028 8.341744
O 5.000000 7.147077 7.650971
H 4.068066 6.942975 7.563761
H 5.380237 6.896963 6.807984
'''

geos['m_cp'] = '''
C 8.074716 8.896609 8.452975
H 8.154933 9.264317 9.473808
H 8.072329 9.738234 7.763478
H 8.921481 8.249858 8.232870
H 7.150122 8.334028 8.341744
X-O 5.000000 7.147077 7.650971
X-H 4.068066 6.942975 7.563761
X-H 5.380237 6.896963 6.807984
'''



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

#with open('res.pkl', 'wb') as f:
#    pickle.dump(res, f)




