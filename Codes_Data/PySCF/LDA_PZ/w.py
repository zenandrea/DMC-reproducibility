#! /usr/bin/env python

import numpy as np
from numpy import array

from pyscf import df, scf, dft

from pyscf import gto 

mol = gto.Mole()
mol.verbose  = 5
mol.atom     = '''
               O    5.00000000   7.14707700   7.65097100
               H    4.06806600   6.94297500   7.56376100
               H    5.38023700   6.89696300   6.80798400
               '''
mol.basis    = 'ccecp-ccpvtz'
mol.unit     = 'A'
mol.ecp      = 'ccecp'
mol.charge   = 0
mol.spin     = 0
mol.symmetry = True
mol.output   = 'w.output'
mol.build()

mf = scf.KS(mol).density_fit()
mf.max_cycle=200
#mf.level_shift=0.0
mf.xc          = 'LDA_X,LDA_C_PZ'
e_scf = mf.kernel()
