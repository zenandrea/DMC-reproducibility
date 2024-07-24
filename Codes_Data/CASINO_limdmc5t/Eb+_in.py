#! /usr/bin/env python3

import os
import pyblock
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sys
#print(sys.argv)
try:
    t = float( sys.argv[1] )
    if t>0 and t<2 :
        taumax = t
    else:
        taumax = 0.1
except:
    taumax = 0.1
print(f'taumax = {taumax}')


makeplot = True # False
viewplot = makeplot

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
        df = df_Eb[ df_Eb.index <= taumax ]
        df2 = df_Ebsc[ df_Ebsc.index <= taumax ]
        plt.figure()
        plt.title(f'{method}')
        plt.axhline(y=-27,color='k',linestyle='--',label='CCSD(T)')
        plt.errorbar(df.index, df.ene, df.err, fmt='^b', label='DMC Eb close-fragments')
        plt.errorbar(df2.index, df2.ene, df2.err, fmt='vr', label='DMC Eb(sc) close-far')
        plt.xlim(0,None)
        plt.xlabel(f'{df_Eb.index.name} /a.u.')
        plt.ylabel('Binding energy /meV')
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'EneDiff/Figin_Eb_{method}.png')
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
        df = df_Esce[ df_Esce.index <= taumax ]
        plt.figure()
        plt.title(f'{method}')
        plt.axhline(y=0,color='k',linestyle='--',label='zero')
        plt.errorbar(df.index, df.ene, df.err, fmt='^b', label='DMC Esce far-fragments')
        plt.xlim(0,None)
        plt.xlabel(f'{df_Esce.index.name} /a.u.')
        plt.ylabel('Size-consistency-error /meV')
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'EneDiff/Figin_Esce_{method}.png')
        if viewplot: plt.show()
  except:
    print(f'WARNING: Missing data for {method}!')

