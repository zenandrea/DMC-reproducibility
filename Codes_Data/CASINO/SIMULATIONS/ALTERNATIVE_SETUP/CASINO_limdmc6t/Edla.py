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

systs = [ 'w' ]
#systs = [ 'w', 'm', 'mw', 'm---w' ]

methods = ['DLA','DLTM','LA0','TM0']
#methods = ['DLA','LA0']

if os.path.isdir('./EneDiffDLA'):
    pass
elif os.path.isfile('./EneDiffDLA'):
    print('Warning: ./EneDiffDLA is a file! Exit')
    exit
else:
    print('Warning: creating the directory ./EneDiffDLA')
    os.mkdir( './EneDiffDLA' )

for syst in systs:
    dfs = {}
    print(f'*** Syst: {syst}')
    try:
        for method in methods:
            print(f'*** Method: {method}')
            if os.path.isfile(f'energy_{syst}_{method}.csv'):
              dfs[method] = pd.read_csv( f'energy_{syst}_{method}.csv',
                      names=['tau','ene','err'], decimal='.', header=None, index_col='tau')
            else:
              dfs[method] = pd.DataFrame({},columns=['tau','ene','err'])
            print(f'dfs[{method}]')
            print(f'{dfs[method]}')
        print(f'\n\n dfs {syst} \n{dfs}\n')

        dla = dfs['DLA']
        #print('DLA',dla)

        la0 = dfs['LA0']
        #print('LA0',la0)

        dltm = dfs['DLTM']
        tm0 = dfs['TM0']
        
        print( '*** Ela = E_dla - E_la0 ***' )
        dla['de0_ene'] = c*(dla.ene-la0.ene)
        dla['de0_err'] = c*(dla.err**2+la0.err**2)**0.5
        df_Ela  = pd.DataFrame([  dla['de0_ene'] ,  dla['de0_err'] ]).T
        df_Ela.sort_index(inplace=True, ascending=False)
        df_Ela.dropna(axis = 0, inplace=True)
        print( df_Ela )
        if len( df_Ela ) > 0:
            df_Ela.to_csv( f'EneDiffDLA/E_dla-la0_{syst}.csv' )
        
        print( '*** Etm = E_dltm - E_tm0 ***' )
        dltm['de0_ene'] = c*(dltm.ene-tm0.ene)
        dltm['de0_err'] = c*(dltm.err**2+tm0.err**2)**0.5
        df_Etm = pd.DataFrame([  dltm['de0_ene'] ,  dltm['de0_err'] ]).T
        df_Etm.sort_index(inplace=True, ascending=False)
        df_Etm.dropna(axis = 0, inplace=True)
        print( df_Etm )
        if len( df_Etm ) > 0:
            df_Etm.to_csv( f'EneDiffDLA/E_dltm-tm0_{syst}.csv' )
        
        
        if makeplot and ( len( df_Ela ) > 0 ):
              plt.figure()
              plt.title(f'{syst}')
              plt.axhline(y=0,color='k',linestyle='--',label='zero')
              plt.errorbar(df_Ela.index, df_Ela.de0_ene, df_Ela.de0_err, fmt='^b', label='DMC E_dla - E_la0')
              plt.errorbar(df_Etm.index, df_Etm.de0_ene, df_Etm.de0_err, fmt='vr', label='DMC E_dltm - E_tm0')
              plt.xlim(0,None)
              plt.xlabel(f'{df_Ela.index.name} /a.u.')
              plt.ylabel('Energy /meV')
              plt.legend()
              plt.tight_layout()
              plt.savefig(f'EneDiffDLA/Fig_E_dla-la0_{syst}.png')
              if viewplot: plt.show()
   
    except:
         print(f'WARNING: Missing data for {syst} {method}!')
