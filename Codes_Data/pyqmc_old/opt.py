import pyqmc.api as pyq
from concurrent.futures import ProcessPoolExecutor
import os.path

if __name__=="__main__":
    with ProcessPoolExecutor(max_workers=40) as client: 
        for directory in ['m','m---w','mw','w']:
            if not os.path.isfile(directory+"/opt_sj.hdf5"):
                pyq.OPTIMIZE(directory+"/mf.hdf5", directory+"/opt_sj.hdf5", nconfig=20000,client=client, npartitions=40, verbose=True)
