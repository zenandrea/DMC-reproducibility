# DMC-codes-comparison
Comparison of the FN-DMC results from different QMC packages, to test reproducibility.

## QMC Packages

1. CASINO https://vallico.net/casinoqmc/
2. QMCPACK https://qmcpack.org/ (https://github.com/QMCPACK/qmcpack)
3. TurboRVB https://turborvb.sissa.it
4. QMC=Chem http://github.com/trex/qmcchem
5. QMeCha https://github.com/QMeCha
6. PyQMC https://github.com/WagnerGroup/pyqmc
7. Amolqc https://github.com/luechow-group/Amolqc
8. QWalk https://github.com/QWalk/mainline
9. CMQMC https://research.csiro.au/mst/tools/cmqmc/
10. CHAMP Cyrus Umrigar's version https://github.com/QMC-Cornell/CHAMP
11. CHAMP Claudia Filippi's version https://www.trex-coe.eu/trex-quantum-chemistry-codes/champ

Others:
* ... suggestions?

## Systems:

The systems under consideration are:

* `m.xyz` methane
* `w.xyz` water
* `mw.xyz` methane-water complex
* `m---w.xyz` methane and water far away, ca. 10 Angstrom 

The coordinates are given in directory `GEOs`.

Notice: 
1. The binding energy __Eb__ is defined as the energy difference between `mw` and `m`+`w`.
2. `m---w` is used to test the size consistency error (__SCE__) at finite timestep, computed as the energy difference between `m---w` and `m`+`w`.

## Setup

* Pseudo: **ccECP** (from, https://pseudopotentiallibrary.org/, copied in local directory `pseudopotentials` on March 29th 2022)
* Basis: **ccECP-ccpVTZ**
* Determinant: DFT Perdew-Zunger **LDA** [J.P.Perdew and A.Zunger, PRB 23, 5048 (1981)] with Slater exchange [J. C. Slater, The Self-Consistent Field for Molecular and Solids, Quantum Theory of Molecular and Solids, Vol. 4 (McGraw-Hill, New York, 1974)].
* Timesteps: as an indication, on CASINO and QMCPACK we used 0.08, 0.04, 0.02, 0.01, 0.005, 0.0025 au.
* Green function modifications: as in indication, on CASINO and QMCPACK we used ZSGMA.
* Notice: DLA and DLTM employs a different Hamiltonian than LA or TM, so the Jastrow parameters in DLA and DLTM should be optimised for the DLA Hamiltonian <img src="https://render.githubusercontent.com/render/math?math=\hat K %2b \hat V_L %2b \frac{\hat V_{NL} {\cal D}}{\cal D}">
<!--- $\hat K + \hat V_L + \frac{\hat V_{NL} {\cal D}}{\cal D}$ --->

For a sanity check, these are the LDA energies obtained for the ccECP pseudo and ccECP-ccpVTZ basis on the `w.xyz` structure:
| Package          | Energy [Ha]        | Directory           |
|:-------          |:------------------ |:---------------     |
| PySCF            | -17.1467579144626  | `PySCF/LDA_PZ/`     |
| Orca 4.2.1       | -17.146744443852   | `Orca/DATA/lda_3Z/` |
| Orca 5.0.3       | -17.146762468465   | `Orca/DATA/lda_3Z_version_5.0.3` |
| Gaussian 09 D.01 | -17.1467613882     | `Gaussian/`         |
| Gaussian 16 B.01 | -17.1467605328     | `Gaussian/`         |

Notice: there were some changes from Orca 4 to Orca 5 (https://wires.onlinelibrary.wiley.com/doi/full/10.1002/wcms.1606),
such as the use of the LibXC library, integration grids, etc. which might explain the difference observed above.  
The determinant obtained from the PySCF LDA calculation, converted to QMCPACK, gives in a VMC calculation w/o Jastrow an energy of -16.93650(5) Ha and a variance of 3.124(5) Ha<sup>2</sup>. An exact calculation with Quantum Package gives -16.9364955292598. 

If case of disagreement, it might be useful to compare the HF energies from DFT codes (PySCF or Orca) with the VMC energy of the converted determinant used w/o Jastrow.
These are the results for the water molecule the ccECP pseudo and ccECP-ccpVTZ basis:
| Method      | Energy [Ha]        | Variance [Ha^2]    | Directory           |
|:-------     |:------------------ |:------------------ |:---------------     |
| HF, PySCF   | -16.9435246665035  |                    | `PySCF/HF/`     |
| VMC, w/o J, QMCPACK  | -16.94351(5) | 3.088(5) | |
| VMC, w/o J, CASINO   | -16.9434(2)  | 3.08(1)  | `PySCF/HF/pyscf2casino` |

After Jastrow optimization the variance should be roughly an order or magnitude smaller. For a comparison, see the energy and variance obtained with QMCPACK, on the LDA determinant, minimising the variance for the standard Hamiltonian in `QMCPACK_complex/vmc_opt.csv`, and for the DLA Hamiltonian in `QMCPACK_complex/vmcDLA_opt.csv`.


## Reporting results and format

Each package has a directory where the results are reported.

Inside the directory there should be files named `energy_{system}_{method}.csv`, reporting on each line comma separated values of the timestep _tau_, the energy and the stochastic error. 
Optionally, report in `var_{system}_{method}.csv` the variance of the local energy in each DMC simulation  

In TurboRVB, instead of the timestep we indicate the mesh value _a_. 
In the comparison betweem DMC and LRDMC we define _a_<sup>2</sup> as an effective _tau_ for LRDMC.

The methods are:
* LA (locality approximation)
* TM (T-move)
* DLA (determinant locality approximation)
* DLTM (determinant locality approximation with T-move)
* LA0 (locality approximation for a trial wave function with no Jastrow, used to test DLA limit)
* TM0 (T-move for a trial wave function with no Jastrow, used to test DLTM limit)

Moreover, in each directory report the input files in a directory named `INPUTS` and indications about how to reproduce the calculations in the file `info.txt`, including the version of the code and the basic setup (target number of walkers, scheme used in the modifications of the Green's function to enhance stability, etc.).

## Analysis

Results from the different packages are collected and analysed by the python script in the directory `Analysis`.

In the final version of the figures below there should be only one set of results for each package, to make it clear.
However, in the testing stage several alternative setups can be tested by using a directory named `{code}_{something}` (e.g., `TurboRVB_sandro`, `QMCPACK_complex`).

We expect to observe the following features:

1. In the DLA scheme, all codes deliver the same total energy, within the stochastic error, in the limit of infinitesimal _tau_ (or infinitesimal _a_ for LRDMC). If differences are observed, they can be due to some numerical errors (cutoffs, etc.). How large are they?

2. Same as in point 1 for the DLTM scheme.

3. A sanity check for the DLA and the DLTM schemes is that the infinitesimal _tau_ limit is the same for different implementations of the Jastrow, and in particular for a calculation with and without Jastrow (notice: without Jastrow DLA is the same as LA, and DLTM is the same as TM). 
    - The sanity check of DLA is passed in TurboRVB, CASINO and QMCPACK.
    - The sanity check of DLTM is passed in TurboRVB, and failed in the present version of CASINO and QMCPACK. There might be a bug. A possible source of this issue is the following: in DLTM the Hamiltonian is <img src="https://render.githubusercontent.com/render/math?math=\hat K %2b \hat V_L %2b \hat V_{NL}^- %2b \frac{\hat V_{NL}^%2b {\cal D}}{\cal D} %2b \hat V_{FN}">, and while the localization of the non-local potential <img src="https://render.githubusercontent.com/render/math?math=\hat V_{NL}^%2B"> is done with the determinant <img src="https://render.githubusercontent.com/render/math?math={\cal D}">, the T-moves on the non-local potential <img src="https://render.githubusercontent.com/render/math?math=\hat V_{NL}^-"> shall be done using the trial wave function <img src="https://render.githubusercontent.com/render/math?math=\psi_T = {\cal D} e^{\cal J}">.

4. The timestep dependence in DLA and DLTM is going to be different in each code, as they implement different functional forms of the Jastrow factor. The modifications to the Green's function to enhance stability (UNR, ZSGMA, ...) will also affect the timestep dependence. Moreover, there are several different implementations of the TM algorith around (Casula 2005, Casula Moroni Sorella Filippi 2010 version 1 and version 2, Anderson Umrigar 2021, ...), yielding different timestep dependencies.

5. In the LA and TM schemes the codes can converge to different total energies, as the Jastrow differs. However, we hope to find agreement in the evaluation of the binging energy. On the timestep dependence, same as in point 4.

6. We might decide to compare also the efficiency of the different codes. For that, I would first look at the Variance, which is an indirect way to assess the quality of the Jastrow factor. In second instance, if we find a common machine where to run a small calculation for each code, we can make a meaningful comparison.


## Preview of preliminary results

<!---
Notice: In the following figure the x values for QMC=Chem are 20*_tau_ (QMC=Chem performs configuration-by-configuration moves, so much smaller _tau_ are used, and if we so not rescale them the results would be squezed on the x-axix). 
--->
Notice: QMC=Chem performs configuration-by-configuration moves, so much smaller _tau_ are used. We might decide to rescale the x-axis for QMC=Chem (e.g., 20*_tau_) to facilitate the comparison with other codes.

* Binding energy ( Eb = E[mw] - E[m] - E[w] )

![Eb](Analysis/Fig_Eb.png)

  As a comparison, the binding energy at the CCSD(T) level, both with all electrons and with ccECP pseudopotentials, the binding is between -25 and -27 meV, and depends mostly on how we do the CBS, see for instance `DMC-codes-comparison/PySCF/CONVERGENCE_ccECP/res_Eb_cp.csv` and results in `DMC-codes-comparison/Orca/DATA_AE/`. In this binding energy, the HF contribution is +8 meV, the CCSD correlation is -29 meV, and the perturbative triple is -5 meV.


* Size consistency error

![SCE](Analysis/Fig_SCE.png)

  The SCE is expected to converge to zero for infinitesimal timestep. It is typically not zero at finite timestep because of the modifications to the Green functon to make DMC stable. For instance, ZSGMA is only approximatively size consistent at finite timestep, while electron by electron modifications to the Green function (as in TurboRVB's LRDMC) can be exactly size consistent.  


* Binding energy with the far away reference ( Eb = E[mw] - E[m---w] )

![Ebsc](Analysis/Fig_Ebsc.png)


* Total energy water, methane and complex

![Energy water](Analysis/Fig_w.png)

![Energy methane](Analysis/Fig_m.png)

![Energy complex methane-water](Analysis/Fig_mw.png)

![Energy methane-water far away](Analysis/Fig_m---w.png)


* Sanity check of the DLA and DLTM implementation

![Sanity check water](Analysis/Fig_w_sanity_DL.png)

  The `DLA` calculations with any Jastrow factor should converge to the same values as for `LA0` (LA w/o Jastrow).
  Similar agreement is expected between `DLTM` and `TM0`. 
  Therefore, the energy differences `DLA-LA0` and the `DLTM-TM0` shall converge to zero for infinitesimal timestep.

## Support calculations

Preparation of the determinant and comparison with results from DFT, HF and Post-HF methods are performed. 
Some results are reported for the following codes, in the corresponding directories:
* PySCF
* Orca
* PWscf

