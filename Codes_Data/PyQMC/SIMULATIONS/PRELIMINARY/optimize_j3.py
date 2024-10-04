import pyqmc.api as pyq
from concurrent.futures import ProcessPoolExecutor
import os.path
import sys
from pyqmc.manybody_jastrow import J3
import numpy as np


if __name__=="__main__":
    directory = sys.argv[1]
    with ProcessPoolExecutor(max_workers=40) as client: 
        if not os.path.isfile(directory+"/opt_sj_j3.hdf5"):
            mol, mf = pyq.recover_pyscf(directory+"/mf.hdf5")
            configs = pyq.initial_guess(mol, 20000)
            jast, to_opt_j = pyq.generate_jastrow(mol)
            mol_dz = mol.copy()
            mol_dz.basis='ccecp-ccpvdz'
            mol_dz.build()
            wf = pyq.MultiplyWF(pyq.generate_slater(mol,mf)[0], jast, J3(mol_dz))
            pyq.read_wf(wf, directory+"/opt_sj2.hdf5")
            to_opt={}
            for k in to_opt_j.keys():
                to_opt['wf2'+k] = to_opt_j[k]
            for k in wf.parameters.keys():
                if 'wf3' in k:
                    to_opt[k] = np.ones_like(wf.parameters[k], dtype=bool)

            for k in to_opt.keys():
               print(k, to_opt[k].shape)
            pgrad = pyq.gradient_generator(mol, wf, to_opt)
            
            pyq.line_minimization(
                wf, 
                configs,
                pgrad,
                client=client,
                npartitions=40,
                verbose=True,
                hdf_file = directory + "/opt_sj_j3.hdf5"
            )
            #pyq.OPTIMIZE(directory+"/mf.hdf5", 
            #             directory+"/opt_sj_j3.hdf5", 
            #             nconfig=40000,
            #             client=client,              
            #             npartitions=40, 
            #             load_parameters=directory+"/opt_sj.hdf5",
            #             verbose=True)
