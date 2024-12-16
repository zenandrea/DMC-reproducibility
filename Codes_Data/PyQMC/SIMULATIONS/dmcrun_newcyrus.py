import pyqmc.api as pyq
from pyqmc.geminaljastrow import GeminalJastrow
import numpy as np
import dla
import argparse
from mpi4py.futures import MPICommExecutor
from mpi4py import MPI
from dmc_trigger_newcyrus import rundmc

def this_rundmc(tstep,
    directory = 'm---w',
    nconfig=20000,
    branchcut_start=10, 
    localization='LA',
    wavefunction='j2',
    feedback=1.0,
    branchtime = 1,
):

    with MPICommExecutor(MPI.COMM_WORLD, root=0) as client:
        mol, mf = pyq.recover_pyscf(directory+"/mf.hdf5", cancel_outputs=False)
        configs = pyq.initial_guess(mol, nconfig)
        jast, to_opt_j = pyq.generate_jastrow(mol)
        if wavefunction=='j2':
            wf = pyq.MultiplyWF(pyq.generate_slater(mol,mf)[0], jast)
            pyq.read_wf(wf, directory+"/optimize_j2_eps1e-2.py.hdf5")
        elif 'j3' in wavefunction:
            mol_dz = mol.copy()
            mol_dz.basis='ccecp-ccpvdz'
            mol_dz.build()
            wf = pyq.MultiplyWF(pyq.generate_slater(mol,mf)[0], jast, GeminalJastrow(mol_dz))
            pyq.read_wf(wf, directory+"/optimize_j2_10000_eps1e-3.py.hdf5")

        if localization == 'LA':
            enacc = dla.LAEnergyAccumulator(mol)
        elif localization == 'DLA':
            enacc = dla.DLAEnergyAccumulator(mol)
        elif localization == 'tmoves':
            enacc = pyq.EnergyAccumulator(mol)
        
        rundmc(
            wf, 
            configs,
            client=client,
            accumulators = {'energy':enacc},
            npartitions=MPI.COMM_WORLD.Get_size()-1,
            verbose=True,
            nsteps_per_block=branchtime,
            tstep=tstep,
            nblocks=int(500000/tstep),
            feedback=feedback,
            hdf_file = directory + f"/newcyrus_{localization}_{wavefunction}_{branchcut_start}_{nconfig}_{tstep}_{feedback}_{branchtime}.hdf5"
        )

if __name__=="__main__":
    parser = argparse.ArgumentParser(
                    prog = 'Run DMC',
                    description = '',
                    epilog = '')
    parser.add_argument('--nconfig',default=2000, type=int)
    parser.add_argument('--branchtime',default=1, type=int)
    parser.add_argument('--wavefunction',default='j3', type=str)
    parser.add_argument('--localization',default='tmoves', type=str)
    parser.add_argument('--directory',default='m---w', type=str)
    parser.add_argument('--feedback',default=1.0, type=float)
    parser.add_argument('--tstep',required=True, type=float)

    #parser.add_argument()
    args=parser.parse_args()
    print(vars(args))
    this_rundmc(**vars(args))
