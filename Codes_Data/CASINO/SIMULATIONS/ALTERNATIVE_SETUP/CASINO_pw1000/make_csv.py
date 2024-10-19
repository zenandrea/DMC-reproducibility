#! /usr/bin/env python3

import pyblock
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt

c = 627.503   # Ha to kcal/mol
c = 27.21138505 * 1e3  # Ha to meV

ntaus = [ '0.100', '0.050', '0.020', '0.010', '0.005', '0.002' ] 
taus = [ float(tau) for tau in ntaus ]

print( f'Timesteps: {taus}' ) 

systs = [ 'W', 'M', 'CLOSE', 'FAR' ]
nsyst = dict( zip(systs,['w','m','mw','m---w']) )

methods = ['LA','TM','DLA','DLTM','LA0','TM0']
dmcPPs = dict( zip( methods, [ 'la', 'tm', 'dla', '', '', '' ] ))


for isyst, syst in enumerate(systs):
    print(f'{isyst}: System {syst}')
    for method in methods:
        dmcPP = dmcPPs[method]
        print(f'*** {method}  DATA/{syst}/LDA_1000/DMC{dmcPP}5_tau ***')
        res = {}
        for i, tau in enumerate(taus):
            dmcdir = f'DATA/{syst}/LDA_1000/DMC{dmcPP}5_{ntaus[i]}'
            filename = f'{dmcdir}/dmc.hist'
            try:
                dmc = np.loadtxt( filename )
                equilibration = int(1.0 / tau)
                data = dmc[equilibration:,3]   # Eloc is on 4th colums, so number 3 for python
                reblock_data = pyblock.blocking.reblock( data )
                opt = pyblock.blocking.find_optimal_block( len(data), reblock_data )
                #print(f'  {syst} ',reblock_data[opt[0]])
                block_size = 2**reblock_data[opt[0]][0]
                energy = reblock_data[0][2]   # use all data
                energy_error = reblock_data[opt[0]][4]
                energy_error_error = reblock_data[opt[0]][5]
                print(f'{tau:8.5f} \t {energy} \t {energy_error} \t {energy_error_error}')
                if ( energy_error < 1.e-3 ):
                    res[tau] = { 'ene': energy, 'err': energy_error }
                else:
                    print(f'Error is too large for tau={tau} in {filename}!')
            except:
                print(f'     Error with {tau}, file {filename}')
                break
        df = pd.DataFrame( res ).T
        #print(df)
        df.to_csv(f'energy_{nsyst[syst]}_{method}.csv', header=False)

