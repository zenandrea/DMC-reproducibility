import pyqmc.api as pyq
from concurrent.futures import ProcessPoolExecutor
import sys
import dla


if __name__=="__main__":
    directory = sys.argv[1]
    tau = float(sys.argv[2])
    loc_approx = sys.argv[3]
    chkfile = directory+"/mf.hdf5"
    mol, mf = pyq.recover_pyscf(chkfile)
    acc = dict(LA=dla.LAEnergyAccumulator, DLA=dla.DLAEnergyAccumulator)[loc_approx](mol)
    with ProcessPoolExecutor(max_workers=40) as client: 
        pyq.DMC(chkfile,
                directory+f"/{loc_approx}dmc{tau}.hdf5", 
                load_parameters=directory+"/opt_sj2.hdf5", 
                nconfig=20000,
                accumulators=dict(energy=False, extra_accumulators={"energy": acc}),
                client=client, 
                npartitions=client._max_workers, 
                tstep=tau,
                nsteps=10000/tau, 
                branchtime=1, 
                verbose=True)
