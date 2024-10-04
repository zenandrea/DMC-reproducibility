#! /usr/bin/env python
import numpy as np
from numpy import array
from pyscf import df, scf, dft
from pyscf import gto 
from pyscf.pbc.tools.pyscf_ase import atoms_from_ase
import ase.io
import os

def run_dft(xyzfile, directory):
    mol = gto.Mole()
    atoms = ase.io.read(xyzfile)
    mol.verbose  = 5
    mol.atom     = atoms_from_ase(atoms)
    mol.basis    = 'ccecp-ccpvtz'
    mol.unit     = 'A'
    mol.ecp      = 'ccecp'
    mol.charge   = 0
    mol.spin     = 0
    mol.symmetry = True
    mol.output   = directory+'/mf.output'
    mol.build()

    mf = scf.KS(mol).density_fit()
    mf.max_cycle=200
    mf.chkfile = directory+'/mf.hdf5'
    #mf.level_shift=0.0
    mf.xc          = 'LDA_X,LDA_C_PZ'
    e_scf = mf.kernel()


if __name__=="__main__":
    from glob import glob
    for f in glob("../GEOs/*.xyz"):
        dirname = f.split('/')[-1].replace('.xyz','')
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        run_dft(f, dirname)