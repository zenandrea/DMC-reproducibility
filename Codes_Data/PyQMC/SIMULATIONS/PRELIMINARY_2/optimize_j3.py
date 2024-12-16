import pyqmc.api as pyq
from concurrent.futures import ProcessPoolExecutor
import os.path
import sys
from pyqmc.j3 import J3
import numpy as np


if __name__=="__main__":
    directory = sys.argv[1]
    with ProcessPoolExecutor(max_workers=40) as client: 
        outfilename = directory+"/opt_sj_j3.hdf5"
        infilename = directory +"/opt_sj2.hdf5"
        if os.path.isfile(outfilename):
            infilename=outfilename
            outfilename = directory+"/opt_sj_j3_second.hdf5"
        if os.path.isfile(outfilename):
            infilename=outfilename
            outfilename = directory+"/opt_sj_j3_third_warmup.hdf5"
        if os.path.isfile(outfilename):
            infilename=outfilename
            outfilename = directory+"/opt_sj_j3_fourth_warmup.hdf5"
        if os.path.isfile(outfilename):
            infilename=outfilename
            outfilename = directory+"/opt_sj_j3_fifth_warmup.hdf5"

        if not os.path.isfile(outfilename):
            mol, mf = pyq.recover_pyscf(directory+"/mf.hdf5")
            configs = pyq.initial_guess(mol, 400000)
            jast, to_opt_j = pyq.generate_jastrow(mol)
            mol_dz = mol.copy()
            mol_dz.basis='ccecp-ccpvdz'
            mol_dz.build()
            wf = pyq.MultiplyWF(pyq.generate_slater(mol,mf)[0], jast, J3(mol_dz))
            to_opt={}
            for k in to_opt_j.keys():
                to_opt['wf2'+k] = to_opt_j[k]
            for k in wf.parameters.keys():
                if 'wf3' in k:
                    to_opt[k] = np.ones_like(wf.parameters[k], dtype=bool)

            pyq.read_wf(wf, infilename)
            pgrad = pyq.gradient_generator(mol, wf, to_opt)
            
            pyq.line_minimization(
                wf, 
                configs,
                pgrad,
                client=client,
                npartitions=40,
                verbose=True,
                warmup_options={'nsteps':1000},	
                hdf_file = outfilename
            )
