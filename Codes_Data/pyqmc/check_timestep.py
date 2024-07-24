import pyqmc.api as pyq
import pandas as pd
from rich import print
import os.path
import matplotlib.pyplot as plt
import seaborn as sns


def get_avg(tstep,
    directory = 'm---w',
    nconfig=20000,
    branchcut_start=10, 
    localization='LA',
    wavefunction='j2',
    feedback=1.0,
    branchtime=1,
    twarmup=10
):

    warmup=int(twarmup/(tstep*branchtime))
    nreblock = 30
    fname = f"{directory}/{localization}_{wavefunction}_{branchcut_start}_{nconfig}_{tstep}_{feedback}_{branchtime}.hdf5"
    print(fname)
    if os.path.isfile(fname):
        print("found")
        return pyq.read_mc_output(fname,warmup=warmup, reblock=nreblock)

    return None


if __name__=="__main__":
    df= []
    for directory in ['m','w','m---w','mw']:
        for tau in [.10, .09, .08, .07, .06, .05, .04,.03, .02, .01, .0075, .005, .0025]:
            for localization in ['DLA','LA','tmoves']:
                for wavefunction in ['j2','j3', 'j3_third']:
                    d = get_avg(directory=directory,tstep=tau, branchcut_start=10, nconfig =2000, wavefunction=wavefunction, localization=localization, branchtime=5)
                    if d is not None:
                        df.append({
                        'system':directory,
                        'tstep':tau,
                        'localization':localization,
                        'wavefunction':wavefunction,
                        'weight_std':d['weight_std'],
                        'energy':d['energytotal'],
                        'error':d['energytotal_err']
                    }) 
    df = pd.DataFrame(df)
    print(df)
    df.to_csv("timesteps.csv", index=False)
