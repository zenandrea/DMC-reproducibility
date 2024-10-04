## PyQMC calculation notes

* The TM moves are performed using Anderson and Umrigar's algorithm. 
* Results are using Sorella's pairing Jastrow, called `j3` in pyqmc
* We used 6 points for the ECP. There are tests under 'naip12' but this did not appear to change anything. 
* We implemented the DLA and LA by modifying the energy accumulators to have no T-moves. These are in `dla.py`


One can reproduce the calculations by running, in order: 

1. `dft.py`
2. `opt.py`
3. `reopt_single.py`
4. `optimize_j3.py`
4. `dmc_dla_j3.py`
5. `dmc_j3.py`

Submit scripts for SLURM are in `reopt_sub.py` and `sub_dmc.py`.


Calculations were performed by 
William Wheeler and Lucas K. Wagner 
Department of Physics
University of Illinois at Urbana-Champaign

Acknowledgement:
Support from the U.S. National Science Foundation via Award No. 1931258 (W.W. and L.K.W.) is acknowledged to develop pyqmc package.