import pandas as pd


df = pd.read_csv("timesteps.csv")
df = df[df.wavefunction == 'j3']
df.rename(columns={'tstep': 'timestep'}, inplace=True)
translations = {'tmoves': 'TM', 'DLA': 'DLA', 'LA': 'LA' } 

for nm, grp in df.groupby(['system']):
    for k, v in translations.items(): 
        tmp = grp[grp.localization == k][['timestep', 'energy', 'error']].copy()
        tmp = tmp[tmp.timestep.isin([.10, .08, .04, .02, .01, .005, .0025])]
        print(f"energy_{nm[0]}_{v}.csv")
        tmp.to_csv(f"energy_{nm[0]}_{v}.csv",index=False, header=False)
