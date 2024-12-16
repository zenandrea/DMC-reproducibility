import pyqmc.api as pyq
import os.path
import sys
import numpy as np
from mpi4py.futures import MPICommExecutor
from mpi4py import MPI


if __name__=="__main__":
    directory = sys.argv[1]
    with MPICommExecutor(MPI.COMM_WORLD, root=0) as client:
        if client is not None:
            outfilename = directory +f"/{os.path.basename(__file__)}.hdf5"

            if not os.path.isfile(outfilename):
                mol, mf = pyq.recover_pyscf(directory+"/mf.hdf5", cancel_outputs=False)
                configs = pyq.initial_guess(mol, 10000)
                wf, to_opt_j = pyq.generate_wf(mol,mf)

                pgrad = pyq.gradient_generator(mol, wf, to_opt_j, eps=1e-3)
                
                pyq.line_minimization(
                    wf, 
                    configs,
                    pgrad,
                    client=client,
                    npartitions=MPI.COMM_WORLD.Get_size()-1,
                    npts=100,
                    verbose=True,
                    warmup_options={'nsteps':1000},	
                    hdf_file = outfilename
                )
