import pyqmc.api as pyq
from concurrent.futures import ProcessPoolExecutor
import sys



if __name__=="__main__":
    directory = sys.argv[1]
    tau = float(sys.argv[2])
    with ProcessPoolExecutor(max_workers=40) as client: 
        pyq.DMC(directory+"/mf.hdf5",
                directory+f"/opt2dmc{tau}.hdf5", 
                load_parameters=directory+"/opt_sj2.hdf5", 
                nconfig=20000,
                client=client, 
                npartitions=40, 
                tstep=tau,
                nsteps=10000/tau, 
                branchtime=1, 
                verbose=True)
