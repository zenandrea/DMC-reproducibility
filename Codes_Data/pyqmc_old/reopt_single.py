import pyqmc.api as pyq
from concurrent.futures import ProcessPoolExecutor
import os.path
import sys


if __name__=="__main__":
    directory = sys.argv[1]
    with ProcessPoolExecutor(max_workers=40) as client: 
        if not os.path.isfile(directory+"/opt_sj2.hdf5"):
            pyq.OPTIMIZE(directory+"/mf.hdf5", 
                         directory+"/opt_sj2.hdf5", 
                         nconfig=40000,
                         client=client,              
                         npartitions=40, 
                         load_parameters=directory+"/opt_sj.hdf5",
                         verbose=True)
