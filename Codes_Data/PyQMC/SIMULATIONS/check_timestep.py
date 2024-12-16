import pyqmc.api as pyq
import pandas as pd
from rich import print
import os.path
import h5py

def get_avg(tstep,
    directory = 'm---w',
    nconfig=20000,
    branchcut_start=10, 
    localization='LA',
    wavefunction='j2',
    feedback=1.0,
    branchtime=1,
    twarmup=2,
    prefix = "",
):

    warmup=int(twarmup/(tstep*branchtime))
    fname = f"{directory}/{prefix}{localization}_{wavefunction}_{branchcut_start}_{nconfig}_{tstep}_{feedback}_{branchtime}.hdf5"
    #print(fname)
    if os.path.isfile(fname):
        #print("found")
        with h5py.File(fname,'r') as f:
            nblocks = f['energytotal'][:].size
        projection_time = nblocks*tstep*branchtime
        if projection_time > 20:
            nreblock = int(min(100, projection_time))
            data =  pyq.read_mc_output(fname,warmup=warmup, reblock=nreblock, exclude_keys=("configs", "weights", "block", "nconfig", "wrap"))
            data['projection_time'] = projection_time
            return data
        else:
            print(f"{fname} skipped: projection time {projection_time}")

    return None


if __name__=="__main__":
    df= []
    for directory in ['m','w','m---w','mw']:
        for tau in [.10, .09, .08, .07, .06, .05, .04,.03, .02, .01, .0075, .005, .0025]:
            for localization in ['DLA','LA','tmoves']:
                for wavefunction in ['j2','j3']:
                    for nconfig in [2000,50000]:
                        d = get_avg(directory=directory,tstep=tau, branchcut_start=10, nconfig =nconfig, wavefunction=wavefunction, localization=localization, branchtime=5, prefix='newcyrus_')
                        if d is not None:
                            df.append({
                            'system':directory,
                            'tstep':tau,
                            'nconfig':nconfig,
                            'localization':localization,
                            'wavefunction':wavefunction,
                            'weight_std':d['weight_std'],
                            'energy':d['energytotal'],
                            'error':d['energytotal_err'],
                            'projection_time':d['projection_time'],
                        }) 
    df = pd.DataFrame(df)
    print(df)
    df.to_csv("timesteps.csv", index=False)
