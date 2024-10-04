import pyqmc.api as pyq
import pandas as pd
import os
df = pd.read_csv("timesteps.csv")
df = df[df.wavefunction=='j3_third']
df.rename(columns={'tstep':'timestep'}, inplace=True)
translations= {'tmoves':'TM', 'DLA':'DLA', 'LA':'LA' } 

for nm, grp in df.groupby(['system']):
    for k, v in translations.items(): 
        tmp = grp[grp.localization==k][['timestep','energy','error']].copy()
        tmp = tmp[tmp.timestep.isin([.10, .08, .04, .02, .01, .005, .0025])]
        tmp.to_csv(f"energy_{nm}_{v}.csv",index=False, header=False)
