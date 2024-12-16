import pyqmc.api as pyq
from concurrent.futures import ProcessPoolExecutor
import os.path
import sys
from pyqmc.geminaljastrow import GeminalJastrow
import numpy as np
from mpi4py.futures import MPICommExecutor
from mpi4py import MPI


if __name__=="__main__":
    directory = sys.argv[1]
    with MPICommExecutor(MPI.COMM_WORLD, root=0) as client:
        outfilename = directory +f"/{os.path.basename(__file__)}.hdf5"
        infilename = directory +"/optimize_j2_eps1e-1.py.hdf5"
        if True:
            mol, mf = pyq.recover_pyscf(directory+"/mf.hdf5", cancel_outputs=False)
            configs = pyq.initial_guess(mol, 10000)
            jast, to_opt_j = pyq.generate_jastrow(mol)
            mol_dz = mol.copy()
            mol_dz.basis='ccecp-ccpvdz'
            mol_dz.build()
            wf = pyq.MultiplyWF(pyq.generate_slater(mol,mf)[0], jast, GeminalJastrow(mol_dz))
            to_opt={}
            for k in to_opt_j.keys():
                to_opt['wf2'+k] = to_opt_j[k]
            for k in wf.parameters.keys():
                if 'wf3' in k:
                    to_opt[k] = np.ones_like(wf.parameters[k], dtype=bool)

            pyq.read_wf(wf, infilename)
            pgrad = pyq.gradient_generator(mol, wf, to_opt, eps=1e-2)
            
            pyq.line_minimization(
                wf, 
                configs,
                pgrad,
                client=client,
                npartitions=MPI.COMM_WORLD.Get_size()-1,
                verbose=True,
                warmup_options={'nsteps':1000},	
                max_iterations = 400,
                hdf_file = outfilename
            )
