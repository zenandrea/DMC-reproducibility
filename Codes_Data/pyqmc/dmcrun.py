import pyqmc.api as pyq
from concurrent.futures import ProcessPoolExecutor
import os.path
import sys
from pyqmc.j3 import J3
import numpy as np
import dla
import argparse

def rundmc(tstep,
    directory = 'm---w',
    nconfig=20000,
    branchcut_start=10, 
    localization='LA',
    wavefunction='j2',
    feedback=1.0,
    branchtime = 1,
    npartitions=40
):

    with ProcessPoolExecutor(max_workers=npartitions) as client: 
        mol, mf = pyq.recover_pyscf(directory+"/mf.hdf5")
        configs = pyq.initial_guess(mol, nconfig)
        jast, to_opt_j = pyq.generate_jastrow(mol)
        if wavefunction=='j2':
            wf = pyq.MultiplyWF(pyq.generate_slater(mol,mf)[0], jast)
            pyq.read_wf(wf, directory+"/opt_sj2.hdf5")
        elif 'j3' in wavefunction:
            mol_dz = mol.copy()
            mol_dz.basis='ccecp-ccpvdz'
            mol_dz.build()
            wf = pyq.MultiplyWF(pyq.generate_slater(mol,mf)[0], jast, J3(mol_dz))
            if 'second' in wavefunction:
                pyq.read_wf(wf, directory+"/opt_sj_j3_second.hdf5")
            elif 'third' in wavefunction:
                if directory == 'm---w':
                    pyq.read_wf(wf, directory+"/opt_sj_j3_fifth_warmup.hdf5")
                else:
                    pyq.read_wf(wf, directory+"/opt_sj_j3_third.hdf5")
                   
            else:
                pyq.read_wf(wf, directory+"/opt_sj_j3.hdf5")

        if localization == 'LA':
            enacc = dla.LAEnergyAccumulator(mol)
        elif localization == 'DLA':
            enacc = dla.DLAEnergyAccumulator(mol)
        elif localization == 'tmoves':
            enacc = pyq.EnergyAccumulator(mol)
        
        pyq.rundmc(
            wf, 
            configs,
            client=client,
            accumulators = {'energy':enacc},
            npartitions=npartitions,
            verbose=True,
            branchtime=branchtime,
            tstep=tstep,
            nsteps=5000/tstep,
            branchcut_start=branchcut_start,
            feedback=feedback,
            hdf_file = directory + f"/{localization}_{wavefunction}_{branchcut_start}_{nconfig}_{tstep}_{feedback}_{branchtime}.hdf5"
        )

if __name__=="__main__":
    parser = argparse.ArgumentParser(
                    prog = 'Run DMC',
                    description = '',
                    epilog = '')
    parser.add_argument('--branchcut_start',default=10, type=float)
    parser.add_argument('--nconfig',default=2000, type=int)
    parser.add_argument('--branchtime',default=1, type=int)
    parser.add_argument('--wavefunction',default='j3', type=str)
    parser.add_argument('--localization',default='tmoves', type=str)
    parser.add_argument('--directory',default='m---w', type=str)
    parser.add_argument('--feedback',default=1.0, type=float)
    parser.add_argument('--tstep',required=True, type=float)
    parser.add_argument('--npartitions',default=40, type=int)

    #parser.add_argument()
    args=parser.parse_args()
    print(vars(args))
    rundmc(**vars(args))
