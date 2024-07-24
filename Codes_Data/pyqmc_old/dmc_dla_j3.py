import pyqmc.api as pyq
from concurrent.futures import ProcessPoolExecutor
import os.path
import sys
from pyqmc.j3 import J3
import numpy as np
import translate_jastrow
import dla

if __name__=="__main__":
    directory = sys.argv[1]
    tstep = float(sys.argv[2])
    with ProcessPoolExecutor(max_workers=40) as client: 
        mol, mf = pyq.recover_pyscf(directory+"/mf.hdf5")
        configs = pyq.initial_guess(mol, 20000)
        jast, to_opt_j = pyq.generate_jastrow(mol)
        jast, to_opt_j = pyq.generate_jastrow(mol)
        mol_dz = mol.copy()
        mol_dz.basis='ccecp-ccpvdz'
        mol_dz.build()
        wf = pyq.MultiplyWF(pyq.generate_slater(mol,mf)[0], jast, J3(mol_dz))
        pyq.read_wf(wf, directory+"/opt_sj_j3.hdf5")
        
        pyq.rundmc(
            wf, 
            configs,
            client=client,
            accumulators = {'energy':dla.DLAEnergyAccumulator(mol)},
            npartitions=40,
            verbose=True,
            branchtime=1,
            tstep=tstep,
            nsteps=10000/tstep, 
            hdf_file = directory + f"/DLAj3dmc{tstep}.hdf5"
        )
