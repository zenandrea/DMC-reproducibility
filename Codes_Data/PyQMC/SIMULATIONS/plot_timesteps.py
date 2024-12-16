import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv("timesteps.csv")
df = df[df['nconfig'] == 50000]
df = df[df['weight_std'] <1]

g = sns.FacetGrid(data=df, col='localization', row='system', hue='wavefunction', sharey=False)
g.map(plt.errorbar, 'tstep','energy', 'error', marker='o', mec='k', mew=1)
g.add_legend()
plt.savefig("timesteps.png", dpi=500)

g = sns.FacetGrid(data=df, col='wavefunction', row='system', hue='localization', sharey=False)
g.map(plt.errorbar, 'tstep','energy', 'error', marker='o', mec='k', mew=1)
g.add_legend()
plt.savefig("timesteps_bywf.png", dpi=500)

def process_group(grp):
    print(grp)
    ens = {}
    err = {}
    scale = 1000*27.2114
    for k in ['mw','m---w', 'm','w']:
        ens[k] = scale*grp[grp['system']==k]['energy'].values[0]
        err[k] = scale*grp[grp['system']==k]['error'].values[0]
    return {
        'size_effect': ens['m---w']-ens['m']-ens['w'],
        'size_effect_err': np.sqrt(err['m---w']**2+err['m']**2+err['w']**2),
        'vdw': ens['mw']-ens['m---w'],
        'vdw_err': np.sqrt(err['m---w']**2+err['mw']**2),
        'vdw_size':ens['mw']-ens['m']-ens['w'],
        'vdw_size_err': np.sqrt(err['mw']**2+err['m']**2+err['w']**2),
    }




grp_names = ['tstep','wavefunction','localization','nconfig']
df_processed = []
for name, group in df.groupby(grp_names):
    print(len(group))
    if len(group) == 4:
        proc = process_group(group)
        for i, k in enumerate(grp_names):
            proc[k] = name[i]
        df_processed.append(proc)
df_processed = pd.DataFrame(df_processed)


g = sns.FacetGrid(data=df_processed, col='wavefunction', hue='localization', sharey=False)
g.map(plt.errorbar, 'tstep','vdw', 'vdw_err', marker='o', mec='k', mew=1)
g.add_legend()
g.set(ylim=(-60,0))
plt.savefig("vdw.png", dpi=500)

g = sns.FacetGrid(data=df_processed, hue='localization', sharey=False)
g.map(plt.errorbar, 'tstep','vdw_size', 'vdw_size_err', marker='o', mec='k', mew=1)
g.add_legend()
g.set(ylim=(-60,0))
plt.savefig("vdw_size.png", dpi=500)

g = sns.FacetGrid(data=df_processed, col='wavefunction', hue='localization', sharey=False)
g.map(plt.errorbar, 'tstep','size_effect', 'size_effect_err', marker='o', mec='k', mew=1)
g.add_legend()
plt.savefig("size.png", dpi=500)
