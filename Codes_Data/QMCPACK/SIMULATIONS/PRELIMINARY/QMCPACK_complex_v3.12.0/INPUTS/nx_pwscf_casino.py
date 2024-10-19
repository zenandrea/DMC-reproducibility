#! /usr/bin/env python3

from nexus import settings,job,run_project,obj
from nexus import ppset
from nexus import generate_physical_system, Structure, PhysicalSystem
from nexus import generate_pyscf, generate_convert4qmc
from nexus import generate_pwscf, generate_pw2qmcpack
from nexus import generate_cusp_correction
from nexus import generate_qmcpack
from generic import obj

# Obtain the core count of the local machine (lab only)
import os
cores = os.cpu_count()
wsname = 'ws'+str(cores)

settings(
    pseudo_dir = './pseudopotentials',
    results    = '',
    sleep      = 3,
    #machine       = wsname,
    machine       = 'andes',
    #machine       = 'summit',
    account       = 'CPH005',
    )

on_desktop = settings.machine==wsname
on_summit  = settings.machine=='summit'
on_andes   = settings.machine=='andes'

print( f'settings.machine = {settings.machine}' )

if on_desktop:
    pwscf_job  = job(cores=cores,app='pw.x')
    conv_job = job(cores=1,app='pw2qmcpack.x')
    qmc_job  = job(cores=1) # fake/placeholder job
    pyscf_job  = job(cores=1)
    c4qmc_job  = job(cores=1)

elif on_summit:
    path_pw = '/ccs/proj/cph005/qe-6.8_patched/build_summit'
    pwscf = f'{path_pw}/bin/pw.x'
    pw2qmcp = f'{path_pw}/bin/pw2qmcpack.x'

    path_qmcp = '/ccs/proj/cph005/QMCPACK/qmcpack-3.12.0'
    qmcpackr = f'{path_qmcp}/bin/qmcpack_legacy_gpu'
    qmcpackc = f'{path_qmcp}/bin/qmcpack_complex_legacy_gpu'

    modules = f'''
BUILD_MODULES={path_qmcp}/config/load_olcf_summit_modules.sh
echo "Purging current module set"
module purge
echo "Sourcing file: $BUILD_MODULES to build QMCPACK"
. $BUILD_MODULES
module list
source activate ~/my_env_summit
'''

    pwscf_job  = job(nodes   = 1,
                   #cores   = 7,
                   #thread = 4,
                   minutes = 120,
                   presub  = modules,
                   app     = pwscf)
    conv_job  = job(nodes   = 1,
                    #cores   = 7,
                    #threads = 4,
                    minutes = 120,
                    presub  = modules,
                    app     = pw2qmcp)
    qmc_job  = job(nodes   = 2,
                   gpus = 6,  # per node
                   alloc_flags = 'gpumps',  # def. smt4, otherwise smt1, smt2
                   minutes = 120,
                   presub  = modules,
                   app     = qmcpackc)
    pyscf_job  = job(nodes   = 1,
                   cores   = 1,
                   thread = 1,
                   minutes = 10,
                   presub  = modules,
                   app     = '/ccs/home/zen/my_env_summit/bin/python' )
    c4qmc_job  = job(nodes   = 1,
                   cores   = 1,
                   thread = 1,
                   minutes = 10,
                   presub  = modules,
                   app     = '/ccs/proj/cph005/QMCPACK/qmcpack-3.12.0/build_summit_cpu/bin/convert4qmc' )

elif on_andes:
    path_pw = '/ccs/proj/cph005/qe-6.8_patched/build_andes'
    pwscf = f'{path_pw}/bin/pw.x -pw2casino'
    pw2qmcp = f'{path_pw}/bin/pw2qmcpack.x'

    path_qmcp = '/ccs/proj/cph005/QMCPACK/qmcpack-3.12.0'
    qmcpackr = f'{path_qmcp}/bin_andes/qmcpack_cpu'
    qmcpackc = f'{path_qmcp}/bin_andes/qmcpack_complex_cpu'

    modules = f'''
#--------------
echo --- Running in `pwd`
echo $MODULESHOME
source $MODULESHOME/init/bash
#--------------
export QMCPACKPATH={path_qmcp}
export NEXUSPATH=$QMCPACKPATH/nexus
BUILD_MODULES=$QMCPACKPATH/config/load_olcf_andes_modules.sh
echo "Purging current module set"
module purge
echo "Sourcing file: $BUILD_MODULES to build QMCPACK"
. $BUILD_MODULES
echo --- Loaded modules
module list
source activate /ccs/home/zen/my_env_andes
# Load QMCPACK tools: Nexus
echo "Adding Nexus to PATH and PYTHONPATH"
export PATH=$NEXUSPATH/bin:$PATH
if [ -z "$PYTHONPATH" ]
then
export PYTHONPATH=$NEXUSPATH/lib
export PYTHONPATH=$QMCPACKPATH/src/QMCTools:$PYTHONPATH
else
export PYTHONPATH=$NEXUSPATH/lib:$PYTHONPATH
export PYTHONPATH=$QMCPACKPATH/src/QMCTools:$PYTHONPATH
fi
#--------------
# https://docs.olcf.ornl.gov/systems/andes_user_guide.html
# Batch Partition Policy (default)
# Bin   Node Count      Duration
# A     1 - 16 Nodes    0 - 48 hr
# B     17 - 64 Nodes   0 - 36 hr
# C     65 - 384 Nodes  0 - 3 hr
# Policy: max 4 jobs running and 4 jobs eligible per user in bins A, B, and C
#--------------

cat << * > pw2casino.dat
&inputpp
 blip_convert=.t.
 blip_binary=.t.
 blip_single_prec=.t.
 blip_multiplicity=1.0
/
*

'''
    pwscf_job  = job(nodes   = 1,
                   #cores   = 7,
                   #thread = 4,
                   minutes = 120,
                   presub  = modules,
                   app     = pwscf )
    conv_job  = job(nodes   = 1,
                    #cores   = 7,
                    #threads = 4,
                    minutes = 120,
                    presub  = modules,
                    app     = pw2qmcp )
    qmc_job  = job(nodes   = 1,  # 16
                   #minutes = 120,
                   hours   =  2,
                   presub  = modules,
                   app     = qmcpackc )
    pyscf_job  = job(nodes   = 1,
                   cores   = 1,
                   thread = 1,
                   minutes = 10,
                   presub  = modules,
                   app     = '/ccs/home/zen/my_env_andes/bin/python' )
    c4qmc_job  = job(nodes   = 1,
                   cores   = 1,
                   thread = 1,
                   minutes = 10,
                   presub  = modules,
                   app     = '/ccs/proj/cph005/QMCPACK/qmcpack-3.12.0/build_andes_cpu/bin/convert4qmc' )

else:
    print('not on desktop or summit!')
    exit()
#end if



nel_val = {
'H' : 1,
'C' : 4,
'N' : 5,
'O' : 6,
#'F' : 7,
#'Cl': 7,
#'Ar': 8,
}
ppset(
    label   = 'ccecp',
    qmcpack = [ f'{atom}.xml' for atom in nel_val ],
    pwscf   = [ f'{atom}.ccECP.upf' for atom in nel_val ],
    )

#lsys = [ 'W', 'M', 'MW' ]
lsys = [ 'W' ]


for i, name in enumerate( lsys ):
    # make an empty structure object
    structure = Structure()
    # read in the xyz file
    structure.read_xyz( f'geo_{name}.xyz' )
    # place a bounding box around the structure
    structure.bounding_box(
        box   = 'cubic',         # cube shaped cell
        mindist = 5,
        recenter=True )
    # make it a gamma point cell
    structure.add_kmesh(
        kgrid      = (1,1,1),    # Monkhorst-Pack grid
        kshift     = (0,0,0),     # and shift
        )
    atoms = set(structure.elem)
    kargs = {}
    for atom in atoms:
        try:
            kargs[atom] = nel_val[atom]
        except:
            print(f'Error: atom {atom} not in list of nel_val')
            break

    # add electronic information
    psystem = PhysicalSystem(
        structure = structure,
        net_charge = 0,          # net charge in units of e
        net_spin   = 0,          # net spin in units of e-spin
        **kargs
        )
#    pp_pwscf = [ f'{atom}.eCEPP.upf' for atom in atoms ]
#    pp_xml   = [ f'{atom}.eCEPP.xml' for atom in atoms ]
#    pp_xml = [ f'{atom}.ccECP.xml' for atom in atoms ]

#    print( f'pp_xml = {pp_xml}' )

    # perform DFT 
    scf = generate_pwscf(
    identifier = 'scf',                         # log output goes to scf.out
    path       = f'{name}/casino_pwSCF1000',         # directory to run in
    job        = pwscf_job,# pyscf must run serially         
    input_type   = 'generic',
    calculation  = 'scf',
    input_dft    = 'lda', 
    ecutwfc      = 1000,   
    conv_thr     = 1e-9, 
    system     = psystem,
    #nogamma = True,   # prevent writing in the format "KPOINTS gamma"
    pseudos    = 'ccecp',
    nosym        = True,
    wf_collect   = True,
    )


    # convert orbitals to QMCPACK format
    conv = generate_pw2qmcpack(
    identifier   = 'conv',
    path       = f'{name}/casino_pwSCF1000',         # directory to run in
    job          = conv_job,
    write_psir   = False,
    dependencies = (scf,'orbitals'),              # Create a dependency to DFT success
    )

    # collect dependencies relating to orbitals
    orbdeps = [(conv,'orbitals' )]



run_project()
   
