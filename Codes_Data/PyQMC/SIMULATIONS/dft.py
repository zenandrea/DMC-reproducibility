#! /usr/bin/env python
import numpy as np
from numpy import array
from pyscf import df, scf, dft
from pyscf import gto 
import ase.io
import os

def ase_atoms_to_pyscf(ase_atoms):
		'''Convert ASE atoms to PySCF atom.

		Note: ASE atoms always use A.
		'''
#return [[ase_atoms.get_chemical_symbols(), ase_atoms.get_positions()] for i, atom in enumerate(ase_atoms)]
		return [ [ase_atoms.get_chemical_symbols()[i], ase_atoms.get_positions()[i]] for i in range(len(ase_atoms.get_positions()))]



def run_dft(xyzfile, directory):
    mol = gto.Mole()
    atoms = ase.io.read(xyzfile)
    mol.verbose  = 5
    mol.atom     = ase_atoms_to_pyscf(atoms)
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
