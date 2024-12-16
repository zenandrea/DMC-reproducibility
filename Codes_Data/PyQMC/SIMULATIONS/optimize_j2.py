import pyqmc.api as pyq
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import os.path
import sys
import numpy as np


if __name__=="__main__":
    directory = sys.argv[1]
    with ProcessPoolExecutor(max_workers=40) as client: 
        outfilename = directory +"/opt_sj2.hdf5"

        if not os.path.isfile(outfilename):
            mol, mf = pyq.recover_pyscf(directory+"/mf.hdf5", cancel_outputs=False)
            configs = pyq.initial_guess(mol, 4000)
            wf, to_opt_j = pyq.generate_wf(mol,mf)

            pgrad = pyq.gradient_generator(mol, wf, to_opt_j)
            
            pyq.line_minimization(
                wf, 
                configs,
                pgrad,
                client=client,
                npartitions=40,
                npts=100,
                verbose=True,
                warmup_options={'nsteps':1000},	
                hdf_file = outfilename
            )
