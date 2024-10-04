import matplotlib.pyplot as plt
import h5py
import numpy as np
import glob 

for fname in ["m/tmoves_j3_10_2000_0.005_1.0_5.hdf5","m/tmoves_j3_10_2000_0.01_1.0_5.hdf5"]:
    with h5py.File(fname,'r') as f:
        en = f['energytotal'][()]
        tstep = f['tstep'][()]
        step = f['step'][()]
    #print(step.shape, tstep.shape, en.shape)
    plt.plot(np.arange(0,en.shape[0])*tstep[0], en, label=fname)

plt.legend()
plt.xlim(0,20)
plt.savefig("energies.png", bbox_inches='tight')

