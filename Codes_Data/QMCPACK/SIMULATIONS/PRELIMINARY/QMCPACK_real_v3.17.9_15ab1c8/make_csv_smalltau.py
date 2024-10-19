#! /usr/bin/env python3

import pyblock
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt

c = 627.503   # Ha to kcal/mol
c = 27.21138505 * 1e3  # Ha to meV

taus = [ 0.005, 0.0025, 0.00125, 0.000625, 0.0003125, 0.00015625 ] 

#systs = [ 'W', 'M', 'MW', 'M---W' ]
#nsyst = dict( zip(systs,['w','m','mw','m---w']) )
systs = [ 'W' ]
nsyst = dict( zip(systs,['w']) )

#dmcPPs = [ 'DLA' ]
#method = dict( zip(dmcPPs,['DLA']) )

methods = ['DLTM','TM0']
dmcPPs = dict( zip( methods, [ 'DLTM','TM' ] ))
dmcdirs = dict( zip( methods, [ 'py_dmc_J3_real_smalltau_new','py_dmc_noJ_real_smalltau_new' ] ) )
#methods = ['DLTM']
#dmcPPs = dict( zip( methods, [ 'DLTM' ] ))
#dmcdirs = dict( zip( methods, [ 'py_dmc_J3_real_smalltau_new' ] ) )

runsdir='DATA/andes_WM_LDA/runs'
#runsdir='DATA/runs'
#runsdir='/Users/zen/Dropbox/project_JAGP_for_nonconvalent/Water-Methane/DATA_SUMMIT/andes_WM_LDA/runs'

for isyst, syst in enumerate(systs):
    print(f'{isyst}: System {syst}')
    for method in methods:
        dmcPP = dmcPPs[method]
        dmcdir = dmcdirs[method]
        print(f'*** {method} {runsdir}/{syst}/{dmcdir}/dmc{dmcPP} ***')
        res = {}
        for i, tau in enumerate(taus):
            #print(f'step {i+1} ) timestep {tau}')
            filename = f'{runsdir}/{syst}/{dmcdir}/dmc{dmcPP}.s00{i+1}.dmc.dat'
            #print( f'    analysis {filename}' )
            try:
                dmc = np.loadtxt( filename )
                equilibration = int(5.0 / tau)
                data = dmc[equilibration:,1]
                reblock_data = pyblock.blocking.reblock( data )
                opt = pyblock.blocking.find_optimal_block( len(data), reblock_data )
                #print(f'  {syst} ',reblock_data[opt[0]])
                block_size = 2**reblock_data[opt[0]][0]
                energy = reblock_data[0][2]   # use all data
                energy_error = reblock_data[opt[0]][4]
                energy_error_error = reblock_data[opt[0]][5]
                #print(f'{tau:8.5f} \t {energy} \t {energy_error} \t {energy_error_error}')
                print(f'{tau:f} \t {energy} \t {energy_error} \t {energy_error_error}')
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

