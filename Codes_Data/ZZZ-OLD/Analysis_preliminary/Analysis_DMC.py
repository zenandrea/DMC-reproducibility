#!/usr/bin/env python
# coding: utf-8

# # Comparing FN-DMC results from several packages

# We made a comparison of local basis sets with splines obtained from plane waves.
# With splines we have a lower energy, because the plane waves with large cutoffs reach the CBS limit. 
# However, the plane waves also imply some other possible error, that we investigated, for instance the Kleinman-Bylander (KB) projection.
# 
# We did some preliminary tests at the HF level, where we can compare the results from the DFT codes (PWscf for the plane-waves, and PySCF for the local basis sets).
# 
# We summarise here the main results obtained.
# 
# ## At the HF level
# 
# The error due to KB is of the order of 0.1 mH (at most it is 0.2 mH) for a water molecule.
# 
# ### PWSCF:
# 
# We performed PWscf calculations with increasing box size, in order to extrapolate the infinite box limit.
# 
# |vacuum [Ang] | E[Hartree] | E [Ry] |
# |-------|:----------:|--------|
# |5| -16.9457| -33.89130774 Ry|
# |6| -16.9456| -33.89121358 Ry|
# |7| -16.9456| -33.89116132 Ry|
# |8| -16.9456| -33.89113008 Ry|
# 
# | Extrapolation | Energy [Hartree]   |
# |---------------|:-------------------|
# |  a+b/x        | -16.9454123926527  |
# |  a+b/x**c     | -16.9455256292671  |
# 
# 
# ### QMCPACK
# 
# These are QMCPACK VMC calculations of the spline wave function (with different values of the mesh factor), where no Jastrow is used, and we use open boundary conditions.
# The difference between this number and the extrapolated value from PWscf is due to the KB approximation in PWscf. 
# 
# ```
# runs/W/pw_VMC/vmcDLA(mf0.5) -16.945313 +/- 0.000041 3.144838 +/- 0.008112 0.1856
# runs/W/pw_VMC/vmcDLAmf0.8   -16.945379 +/- 0.000041 3.081212 +/- 0.001959 0.1818
# runs/W/pw_VMC/vmcDLAmf1.0   -16.945364 +/- 0.000044 3.076979 +/- 0.002666 0.1816
# ```
# 
# ### PySCF
# 
# This is the convergence of the HF energy for increasing basis set size.
# 
# ```
# runs/W_ccecp-ccpvdz/SCF/scf.output:converged SCF energy = -16.9328784437541
# runs/W_ccecp-ccpvtz/SCF/scf.output:converged SCF energy = -16.9435246665035
# runs/W_ccecp-ccpvqz/SCF/scf.output:converged SCF energy = -16.9448965250943
# runs/W_ccecp-ccpv5z/SCF/scf.output:converged SCF energy = -16.9452271890764
# runs/W_ccecp-ccpv6z/SCF/scf.output:converged SCF energy = -16.9453580187172
# runs/W_ccecp-augccpvdz/SCF/scf.output:converged SCF energy = -16.9403270111112
# runs/W_ccecp-augccpvtz/SCF/scf.output:converged SCF energy = -16.9446290867156
# runs/W_ccecp-augccpvqz/SCF/scf.output:converged SCF energy = -16.945274829488
# runs/W_ccecp-augccpv5z/SCF/scf.output:converged SCF energy = -16.9453732259853
# runs/W_ccecp-augccpv6z/SCF/scf.output:converged SCF energy = -16.945423505628
# ```
# 
# ### Pyscf-QMCPACK & PWscf-QMCPACK on ccecp-ccpvtz
# ```
# Pyscf           -16.9435246665035
# py_VMC          -16.943510(49)     Var[E_L] = 3.0876(54)
# ---
# PWscf extrap.   -16.9455256292671
# pw_VMC mf=0.5   -16.945313(41)                3.1448(81) 
# pw_VMC mf=0.8   -16.945379(41)                3.0812(19) 
# pw_VMC mf=1.0   -16.945364(44)                3.0770(27) 
# ```
# So, wave function from PWscf+splines is better than the w.f. from the ccecp-ccpvtz basis by ca. **2 mH**!
# 
# **TO DO: TEST CASINO, with single and double mesh in splines, and with single and double precision**

# In[1]:


import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO


# In[2]:


colors = {
    'TurboRVB' : 'red',
    'CASINO'   : 'green',
    'CASINO_limdmc5'   : 'brown',
    'QMCPACK'  : 'blue',
    'CHAMP-CF' : 'blueviolet', # set here the final name for Claudia Filippi's version
    'CHAMP-CU' : 'magenta',    # set here the final name for Cyrus Umrigar's version
    'QMC=Chem' : 'cyan',
    'QMeCha'   : 'orange',
    'PyQMC'    : 'black',
    'Amolqm'   : 'gold',
    'QWalk'    : 'olive',
    'CMQMC'    : 'darkgray',
}

codes = list( colors.keys() )


systems = [ 'm', 'w', 'mw', 'm---w' ]
methods = [ 'LA', 'TM', 'DLA', 'DLTM' ]

syst_names = dict(zip(systems,['methane','water','complex','far']))

colors_opt = {
    'TurboRVB_sandro'  : 'tomato',
    'QMCPACK_complex'  : 'skyblue',
    'CASINO_pw1000'    : 'lime',
    'CASINO_pw1000_andes' : 'mediumseagreen',
}
methods_opt = ['LA0', 'TM0']
codes_opt = list( colors_opt.keys() )
colors_all = { **colors, **colors_opt }

codes_all = codes + codes_opt


# In[3]:


# Test reading csv
d = pd.read_csv('../QMC=Chem/energy_w_DLA.csv',
                  names=['a','ene','err'], decimal='.',
                  header=None)
#d['tau'] = d.a**2
d.index = d.a
d.index.name = 'tau'
d

dd = pd.DataFrame([d.ene,d.err]).T
dd


# In[4]:


# Test reading csv
d = pd.read_csv('../QWalk/energy_w_LA.csv',
                  names=['a','ene','err'], decimal='.',
                  header=None)
#d['tau'] = d.a**2
d.index = d.a
d.index.name = 'tau'
d

dd = pd.DataFrame([d.ene,d.err]).T
dd


# In[5]:


# TurboRVB results obtained with
# psuudo: ccECP
# basis: cc_pVTZ
# J. basis: O:3s1p, C:3s1p, H:3s

data = {}
for code in codes+codes_opt:
    data[code] = {}

for code in codes+codes_opt:
    if code.startswith('TurboRVB'):
        names = ['a','ene','err']
    else:
        names = ['tau','ene','err']
    for method in methods+methods_opt:
        for syst in systems:
            key = f'{syst}_{method}'
            try: 
                data[code][key] = pd.read_csv(
                    f'../{code}/energy_{key}.csv',
                    names=names, decimal='.',
                    header=None, index_col=names[0] )
            except:
                data[code][key] = None
                
#data["TurboRVB"]
#data["QMCPACK"]
data["QMC=Chem"]


# In[6]:


# Set the x value for the plots 
# most codes: x <- tau
# Turborvb:   x <- alar^2
# QMC=Chem:   x <- 20*tau
# because in QMC=Chem (where there are single-electron moves)
# tau is too small for a comparison in the plots


def x_axis( df, code ):
    x = np.array( df.index )
    if code.startswith('TurboRVB'):
        xnew = x**2
    elif code.startswith('QMC=Chem'):
        xnew = x * 20
    else:
        xnew = x
    return xnew

#for code in data:
#    print(code)
#    d = data[code]
#    for calc in d:
#        df = d[calc]
#        try:
#            if code.startswith('TurboRVB'):
#                df['x'] = df.index**2
#            elif code.startswith('QMC=Chem'):
#                df['x'] = df.index * 20
#            else:
#                df['x'] = df.index
#        except:
#            pass
 
#data['QMC=Chem']['mw_DLA']
#data['TurboRVB']['mw_DLA']
#print(x_axis(data['QMCPACK']['mw_DLA'], 'QMCPACK'))


# In[7]:


# Compute binding energies

# Hartree to meV
c = 27.211396641308*1000

for code in codes+codes_opt:
    datac = data[code]
    for method in methods:
        try:
            m = datac[f'm_{method}']
            w = datac[f'w_{method}']
            mw = datac[f'mw_{method}']
            Eb = c*(mw.ene-m.ene-w.ene)
            Eb_err = c*(mw.err**2+m.err**2+w.err**2)**0.5
            df_Eb = pd.DataFrame([Eb, Eb_err]).T
            #print(df_Eb)
            datac[f'Eb_{method}'] = df_Eb
        except:
            pass

#data["TurboRVB"]['Eb_DLA']
#data['QMCPACK_complex']['Eb_DLA']
#data['QMC=Chem']['Eb_DLA']


# In[56]:


fig, ax = plt.subplots(1,4, figsize=(15,5), sharey=True, sharex=True )

ax[0].set_ylabel( 'Binding Energy [meV]' )
for i, method in enumerate(methods):
    ax[i].set_xlim(0,0.17)
    ax[i].set_xlabel( r'DMC $\tau$ or LRDMC $a^2$ [a.u.]' )
    for code in codes:
        try:
            datac = data[code][f'Eb_{method}']
            x = x_axis( datac, code )
            y = datac.ene
            y_err = datac.err
            ax[i].errorbar( x, y, y_err, fmt='o:', 
                           label=code, color=colors_all[code] )
        except:
            print(f'Exception for method {method} code {code}')
            pass
    ax[i].axhline(y=-27,color='black',ls='--',label='CCSD(T)')
    ax[i].label_outer()

ax[0].set_title('Locality approximation')
ax[1].set_title('T-move')
ax[2].set_title('Determinant locality approximation')
ax[3].set_title('Determinant locality T-move')

#ax[1].set_title('Water')
#ax[0].legend(loc=1)
#ax[1].legend()
#ax[2].legend()
#ax[3].legend()
#handles, labels = ax[2].get_legend_handles_labels()
#fig.legend(labels=labels, handles=handles, ncol=1, loc='center', bbox_to_anchor=( 1.05, 0.5))


leg = {}
for i in range(4): 
    handles, labels = ax[i].get_legend_handles_labels()
    for j in range(len(labels)):
        leg[labels[j]] = handles[j]
import collections
leg = collections.OrderedDict(sorted(leg.items()))
aus = leg['CCSD(T)']; del(leg['CCSD(T)']); leg['CCSD(T)']=aus
legend_outside = fig.legend(labels=list(leg.keys()), handles=list(leg.values()), ncol=1, loc='center', bbox_to_anchor=( 1.05, 0.5))


plt.tight_layout()
fig.savefig('Fig_Eb.png',bbox_extra_artists=(legend_outside,),bbox_inches='tight')


# In[31]:


print(leg.keys())


# In[39]:


# Hartree to meV
c = 27.211396641308*1000

# compute the size consistency error (SCE)
for code in codes+codes_opt:
    datac = data[code]
    for method in methods:
        try:
            m = datac[f'm_{method}']
            w = datac[f'w_{method}']
            far = datac[f'm---w_{method}']
            Eb = c*(far.ene-m.ene-w.ene)
            Eb_err = c*(far.err**2+m.err**2+w.err**2)**0.5
            df_Eb = pd.DataFrame([Eb, Eb_err]).T
            #print(df_Eb)
            datac[f'SCE_{method}'] = df_Eb
        except:
            pass

#data['TurboRVB']['SCE_DLA']


# In[55]:


fig, ax = plt.subplots(1,4, figsize=(15,5), sharey=True, sharex=True )

ax[0].set_ylabel( 'Size Consistency Error [meV]' )
for i, method in enumerate(methods):
    ax[i].set_xlim(0,0.17)
    ax[i].set_xlabel( r'DMC $\tau$ or LRDMC $a^2$ [a.u.]' )
    for code in codes:
        try:
            datac = data[code][f'SCE_{method}']
            x = x_axis( datac, code )
            y = datac.ene
            y_err = datac.err
            ax[i].errorbar( x, y, y_err, fmt='o:', 
                           label=code, color=colors_all[code] )
        except:
            pass
    ax[i].axhline(y=0.0,color='black',ls='--')

ax[0].set_title('Locality approximation')
ax[1].set_title('T-move')
ax[2].set_title('Determinant locality approximation')
ax[3].set_title('Determinant locality T-move')

#ax[1].set_title('Water')
#ax[0].legend(loc=1)
#ax[1].legend()
#ax[2].legend()
#ax[3].legend()


leg = {}
for i in range(4): 
    handles, labels = ax[i].get_legend_handles_labels()
    for j in range(len(labels)):
        leg[labels[j]] = handles[j]
import collections
leg = collections.OrderedDict(sorted(leg.items()))
#aus = leg['CCSD(T)']; del(leg['CCSD(T)']); leg['CCSD(T)']=aus
legend_outside = fig.legend(labels=list(leg.keys()), handles=list(leg.values()), ncol=1, loc='center', bbox_to_anchor=( 1.05, 0.5))


plt.tight_layout()
fig.savefig('Fig_SCE.png',bbox_extra_artists=(legend_outside,),bbox_inches='tight')


# In[42]:


# Hartree to meV
c = 27.211396641308*1000

# compute the binding enegy in a size consistency way
# Ebsc = E[mw] - E[m---w]
for code in codes+codes_opt:
    datac = data[code]
    for method in methods:
        try:
            close = datac[f'mw_{method}']
            far = datac[f'm---w_{method}']
            Eb = c*(close.ene-far.ene)
            Eb_err = c*(close.err**2+far.err**2)**0.5
            df_Eb = pd.DataFrame([Eb, Eb_err]).T
            #print(df_Eb)
            datac[f'Ebsc_{method}'] = df_Eb
        except:
            pass

#data['TurboRVB']['Ebsc_DLA']
data['QMC=Chem']['Ebsc_DLA']


# In[54]:


fig, ax = plt.subplots(1,4, figsize=(15,5), sharey=True, sharex=True )

ax[0].set_ylabel( 'Binding Energy [meV]' )
for i, method in enumerate(methods):
    ax[i].set_xlim(0,0.17)
    ax[i].set_xlabel( r'DMC $\tau$ or LRDMC $a^2$ [a.u.]' )
    for code in codes:
        try:
            datac = data[code][f'Ebsc_{method}']
            x = x_axis( datac, code )
            y = datac.ene
            y_err = datac.err
            ax[i].errorbar( x, y, y_err, fmt='o:', 
                           label=code, color=colors_all[code] )
        except:
            pass
    ax[i].axhline(y=-27,color='black',ls='--',label='CCSD(T)')

ax[0].set_title('Locality approximation')
ax[1].set_title('T-move')
ax[2].set_title('Determinant locality approximation')
ax[3].set_title('Determinant locality T-move')

#ax[1].set_title('Water')
#ax[0].legend(loc=1)
#ax[1].legend()
#ax[2].legend()
#ax[2].legend()


leg = {}
for i in range(4): 
    handles, labels = ax[i].get_legend_handles_labels()
    for j in range(len(labels)):
        leg[labels[j]] = handles[j]
import collections
leg = collections.OrderedDict(sorted(leg.items()))
aus = leg['CCSD(T)']; del(leg['CCSD(T)']); leg['CCSD(T)']=aus
legend_outside = fig.legend(labels=list(leg.keys()), handles=list(leg.values()), ncol=1, loc='center', bbox_to_anchor=( 1.05, 0.5))


plt.tight_layout()
fig.savefig('Fig_Ebsc.png',bbox_extra_artists=(legend_outside,),bbox_inches='tight')


# In[53]:


for syst in systems:
    fig, ax = plt.subplots(1,4, figsize=(15,5), sharey=True, sharex=True )

    ax[0].set_ylabel( f'Energy {syst_names[syst]} [Ha]' )
    for i, method in enumerate(methods):
        ax[i].set_xlim(0,0.17)
        ax[i].set_xlabel( r'DMC $\tau$ or LRDMC $a^2$ [a.u.]' )
        for code in codes:
            try:
                datac = data[code][f'{syst}_{method}']
                x = x_axis( datac, code )
                y = datac.ene
                y_err = datac.err
                ax[i].errorbar( x, y, y_err, fmt='o:', 
                               label=code, color=colors_all[code] )
            except:
                pass

    ax[0].set_title('Locality approximation')
    ax[1].set_title('T-move')
    ax[2].set_title('Determinant locality approximation')
    ax[3].set_title('Determinant locality T-move')

    #ax[1].set_title('Water')
    #ax[0].legend(loc=1)
    #ax[1].legend()
    #ax[2].legend()
    #ax[3].legend()

    
    leg = {}
    for i in range(4): 
        handles, labels = ax[i].get_legend_handles_labels()
        for j in range(len(labels)):
            leg[labels[j]] = handles[j]
    import collections
    leg = collections.OrderedDict(sorted(leg.items()))
    #aus = leg['CCSD(T)']; del(leg['CCSD(T)']); leg['CCSD(T)']=aus
    legend_outside = fig.legend(labels=list(leg.keys()), handles=list(leg.values()), ncol=1, loc='center', bbox_to_anchor=( 1.05, 0.5))


    plt.tight_layout()
    fig.savefig(f'Fig_{syst}.png',bbox_extra_artists=(legend_outside,),bbox_inches='tight')


# In[52]:


for syst in systems:
    fig, ax = plt.subplots(1,4, figsize=(15,5), sharey=True, sharex=True )

    ax[0].set_ylabel( f'Energy {syst_names[syst]} [Ha]' )
    for i, method in enumerate(methods):
        ax[i].set_xlim(0,0.17)
        ax[i].set_xlabel( r'DMC $\tau$ or LRDMC $a^2$ [a.u.]' )
        for code in codes+codes_opt:
            try:
                datac = data[code][f'{syst}_{method}']
                x = x_axis( datac, code )
                y = datac.ene
                y_err = datac.err
                ax[i].errorbar( x, y, y_err, fmt='o:', 
                               label=code, color=colors_all[code] )
            except:
                pass
    for j, method in enumerate(methods_opt):
        i = 2+j
        for code in codes+codes_opt:
            try:
                datac = data[code][f'{syst}_{method}']
                x = x_axis( datac, code )
                y = datac.ene
                y_err = datac.err
                ax[i].errorbar( x, y, y_err, fmt='^:', 
                               label=code+' No J.', 
                               color=colors_all[code],
                               markeredgecolor=colors_all[code],
                               markerfacecolor=None )
            except:
                pass

    ax[0].set_title('Locality approximation')
    ax[1].set_title('T-move')
    ax[2].set_title('Determinant locality approximation')
    ax[3].set_title('Determinant locality T-move')

    #ax[2].legend()

    
    leg = {}
    for i in range(4): 
        handles, labels = ax[i].get_legend_handles_labels()
        for j in range(len(labels)):
            leg[labels[j]] = handles[j]
    import collections
    leg = collections.OrderedDict(sorted(leg.items()))
    #aus = leg['CCSD(T)']; del(leg['CCSD(T)']); leg['CCSD(T)']=aus
    legend_outside = fig.legend(labels=list(leg.keys()), handles=list(leg.values()), ncol=1, loc='center', bbox_to_anchor=( 1.05, 0.5))


    plt.tight_layout()
    fig.savefig(f'Fig_{syst}_wNoJ.png',bbox_extra_artists=(legend_outside,),bbox_inches='tight')


# In[51]:


method2={}
method2['DLA']='LA0'
method2['DLTM']='TM0'

for syst in systems:
    fig, ax = plt.subplots(1,2, figsize=(8,5), sharey=True, sharex=True )

    ax[0].set_ylabel( f'Energy diff. w & w/o J. {syst_names[syst]} [Ha]' )
    for i, method in enumerate(['DLA','DLTM']):
        ax[i].axhline(y=0.0,color='black',ls='--',label='')
        ax[i].set_xlim(0,0.17)
        ax[i].set_xlabel( r'DMC $\tau$ or LRDMC $a^2$ [a.u.]' )
        for code in codes+codes_opt:
            try:
                datac1 = data[code][f'{syst}_{method}']
                datac0 = data[code][f'{syst}_{method2[method]}']
                datac = datac1 - datac0
                datac.err = (( datac1.err**2 + datac0.err**2 )**0.5)
                #print(code,method,'\n',datac0,datac1,datac)
                x = x_axis( datac, code )
                y = datac.ene
                y_err = datac.err
                ax[i].errorbar( x, y, y_err, fmt='o:', 
                               label=code, color=colors_all[code] )
            except:
                pass

    ax[0].set_title('Determinant locality approximation')
    ax[1].set_title('Determinant locality T-move')

    #ax[0].legend()

    
    leg = {}
    for i in range(2): 
        handles, labels = ax[i].get_legend_handles_labels()
        for j in range(len(labels)):
            leg[labels[j]] = handles[j]
    import collections
    leg = collections.OrderedDict(sorted(leg.items()))
    #aus = leg['CCSD(T)']; del(leg['CCSD(T)']); leg['CCSD(T)']=aus
    legend_outside = fig.legend(labels=list(leg.keys()), handles=list(leg.values()), ncol=1, loc='center', bbox_to_anchor=( 1.05, 0.5))


    fig.tight_layout()
    fig.savefig(f'Fig_{syst}_sanity_DL.png',bbox_extra_artists=(legend_outside,),bbox_inches='tight')


# In[ ]:





# In[ ]:





# In[ ]:




