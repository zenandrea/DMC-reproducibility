import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv("timesteps.csv")

g = sns.FacetGrid(data=df, col='localization', row='system', hue='wavefunction', sharey=False)
g.map(plt.errorbar, 'tstep','energy', 'error', marker='o', mec='k', mew=1)
g.add_legend()
plt.savefig("timesteps.png", dpi=500)

g = sns.FacetGrid(data=df, col='wavefunction', row='system', hue='localization', sharey=False)
g.map(plt.errorbar, 'tstep','energy', 'error', marker='o', mec='k', mew=1)
g.add_legend()
plt.savefig("timesteps_bywf.png", dpi=500)