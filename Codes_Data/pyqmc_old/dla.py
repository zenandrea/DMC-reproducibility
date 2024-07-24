# determinant localization approximation
# for the localization approximation, instead of :math:`\frac{V_{nl} \Psi}{\Psi}` use just the determinant :math:`\frac{V_{nl} \mathcal{D}}{\mathcal{D}}`
# The localization approximation can be done just by defining an energy accumulator with has_nonlocal_moves to be False, and doesn't require modifying the codebase.
# For determinant localization, we pass only the Slater part of the wf to the ecp evaluator
import pyqmc.energy as energy
import pyqmc.eval_ecp as eval_ecp
import pyqmc.ewald as ewald
import pyqmc.gpu as gpu
import numpy as np


class DLAEnergyAccumulator:
    """Returns local energy of each configuration in a dictionary."""

    def __init__(self, mol, threshold=10, **kwargs):
        self.mol = mol 
        self.threshold = threshold
        if hasattr(mol, "a"):
            self.coulomb = ewald.Ewald(mol, **kwargs)
        else:
            self.coulomb = energy.OpenCoulomb(mol, **kwargs)

    def __call__(self, configs, wf):
        ee, ei, ii = self.coulomb.energy(configs)
        ecp_val = eval_ecp.ecp(self.mol, configs, wf.wf_factors[0], self.threshold)
        ke, grad2 = energy.kinetic(configs, wf) 
        return {
            "ke": ke, 
            "ee": ee, 
            "ei": ei, 
            "ecp": ecp_val,
            "grad2": grad2,
            "total": ke + ee + ei + ecp_val + ii, 
        }   

    def avg(self, configs, wf):
        return {k: np.mean(it, axis=0) for k, it in self(configs, wf).items()}

    def has_nonlocal_moves(self):
        return False

    def keys(self):
        return set(["ke", "ee", "ei", "ecp", "total", "grad2"])

    def shapes(self):
        return {"ke": (), "ee": (), "ei": (), "ecp": (), "total": (), "grad2": ()} 


class LAEnergyAccumulator:
    """Returns local energy of each configuration in a dictionary."""

    def __init__(self, mol, threshold=10, **kwargs):
        self.mol = mol 
        self.threshold = threshold
        if hasattr(mol, "a"):
            self.coulomb = ewald.Ewald(mol, **kwargs)
        else:
            self.coulomb = energy.OpenCoulomb(mol, **kwargs)

    def __call__(self, configs, wf):
        ee, ei, ii = self.coulomb.energy(configs)
        ecp_val = eval_ecp.ecp(self.mol, configs, wf, self.threshold)
        ke, grad2 = energy.kinetic(configs, wf) 
        return {
            "ke": ke, 
            "ee": ee, 
            "ei": ei, 
            "ecp": ecp_val,
            "grad2": grad2,
            "total": ke + ee + ei + ecp_val + ii, 
        }   

    def avg(self, configs, wf):
        return {k: np.mean(it, axis=0) for k, it in self(configs, wf).items()}

    def has_nonlocal_moves(self):
        return False

    def keys(self):
        return set(["ke", "ee", "ei", "ecp", "total", "grad2"])

    def shapes(self):
        return {"ke": (), "ee": (), "ei": (), "ecp": (), "total": (), "grad2": ()} 


