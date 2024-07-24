#! /usr/bin/env python3

import os
import pyblock
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

makeplot = True # False
viewplot = False # makeplot

c = 627.503   # Ha to kcal/mol
c = 27.21138505 * 1e3  # Ha to meV

systs = [ 'w', 'm', 'mw', 'm---w' ]

#methods = ['DLA']
methods = ['LA','TM','DLA','DLTM','LA0','TM0']

if os.path.isdir('./EneDiff'):
    pass
elif os.path.isfile('./EneDiff'):
    print('Warning: ./EneDiff is a file! Exit')
    exit
else:
    print('Warning: creating the directory ./EneDiff')
    os.mkdir( './EneDiff' )

for method in methods:
  try:
    print(f'*** Method: {method}')
    dfs = {}
    for syst in systs:
      if os.path.isfile(f'energy_{syst}_{method}.csv'):
        dfs[syst] = pd.read_csv( f'energy_{syst}_{method}.csv',
                names=['tau','ene','err'], decimal='.', header=None, index_col='tau')
      else:
        dfs[syst] = pd.DataFrame({},columns=['tau','ene','err'])
    A   = dfs['m']
    B   = dfs['w']
    AB  = dfs['mw']
    A_B = dfs['m---w']
    #print("A = \n",A,"\nB = \n",B,"\nAB = \n",AB,"\nA_B = \n",A_B)

    print( '*** Eb = close - fragments ***' )
    Eb     = c*(AB.ene-A.ene-B.ene)
    Eb_err = c*(AB.err**2+A.err**2+B.err**2)**0.5
    df_Eb = pd.DataFrame([Eb, Eb_err]).T
    df_Eb.sort_index(inplace=True, ascending=False)
    df_Eb.dropna(axis = 0, inplace=True)
    print( df_Eb )
    if len( df_Eb ) > 0:
        df_Eb.to_csv( f'EneDiff/Eb_{method}.csv' )
    print( '*** Ebsc = close - far ***' )
    Eb     = c*(AB.ene-A_B.ene)
    Eb_err = c*(AB.err**2+A_B.err**2)**0.5
    df_Ebsc = pd.DataFrame([Eb, Eb_err]).T
    df_Ebsc.sort_index(inplace=True, ascending=False)
    df_Ebsc.dropna(axis = 0, inplace=True)
    print( df_Ebsc )
    if len( df_Ebsc ) > 0:
        df_Ebsc.to_csv( f'EneDiff/Ebsc_{method}.csv' )

    if makeplot and ( len( df_Eb ) > 0 or len( df_Ebsc ) > 0 ):
        plt.figure()
        plt.title(f'{method}')
        plt.axhline(y=-27,color='k',linestyle='--',label='CCSD(T)')
        plt.errorbar(df_Eb.index, df_Eb.ene, df_Eb.err, fmt='^b', label='DMC Eb close-fragments')
        plt.errorbar(df_Ebsc.index, df_Ebsc.ene, df_Ebsc.err, fmt='vr', label='DMC Eb(sc) close-far')
        plt.xlim(0,None)
        plt.xlabel(f'{df_Eb.index.name} /a.u.')
        plt.ylabel('Binding energy /meV')
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'EneDiff/Fig_Eb_{method}.png')
        if viewplot: plt.show()

    print( '*** Esce = far - fragments ***' )
    Eb     = c*(A_B.ene-A.ene-B.ene)
    Eb_err = c*(A_B.err**2+A.err**2+B.err**2)**0.5
    df_Esce = pd.DataFrame([Eb, Eb_err]).T
    df_Esce.sort_index(inplace=True, ascending=False)
    df_Esce.dropna(axis = 0, inplace=True)
    print( df_Esce )
    if len( df_Esce ) > 0:
        df_Esce.to_csv( f'EneDiff/Esce_{method}.csv' )

    if makeplot and ( len( df_Esce ) > 0 ):
        plt.figure()
        plt.title(f'{method}')
        plt.axhline(y=0,color='k',linestyle='--',label='zero')
        plt.errorbar(df_Esce.index, df_Esce.ene, df_Esce.err, fmt='^b', label='DMC Esce far-fragments')
        plt.xlim(0,None)
        plt.xlabel(f'{df_Esce.index.name} /a.u.')
        plt.ylabel('Size-consistency-error /meV')
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'EneDiff/Fig_Esce_{method}.png')
        if viewplot: plt.show()
  except:
    print(f'WARNING: Missing data for {method}!')

