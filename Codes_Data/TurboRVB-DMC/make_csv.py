#! /usr/bin/env python3

import pyblock
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt

c = 627.503   # Ha to kcal/mol
c = 27.21138505 * 1e3  # Ha to meV

dsys = {}
dsys['w'] = '01water'
dsys['m'] = '02methane'
dsys['m---w'] = '03complex_far_away'
dsys['mw'] = '04complex_bound'
sys = list(dsys)
#systs = [ 'w', 'm', 'mw', 'm---w' ]

#methods = ['LA','TM','DLA','DLTM','LA0','TM0']
methods = ['TM']


DATA='../TurboRVB.DATA'

for isyst, syst in enumerate(sys):
    print(f'{isyst}: System {syst}')
    for method in methods:
        #file = f'{DATA}/{dsys[syst]}/dmc_jdft_tmove/storage/envstau_clean.dat'
        file = f'{DATA}/{dsys[syst]}/dmc_jdft_tmove2/storage/envstau.dat'
        print(file)
        df = pd.DataFrame( np.loadtxt( file ), columns = ('tau','ene','err') )
        df = df.loc[ df.err < 1.e-3 ]
        df.to_csv(f'energy_{syst}_{method}.csv', header=False, index=False)

