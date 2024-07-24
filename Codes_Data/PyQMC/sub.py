#!/usr/bin/env python3
import sys
import uuid
import os
import pyqmc.api as pyq
queue = 'qmchamm'
ncores=40

def submit_dmc(**kwargs):
    subname = "sub/" + str(uuid.uuid4())
    jobname="".join(f"{v}" for k,v in kwargs.items())
    args =" ".join(f"--{k} {v}" for k,v in kwargs.items())
    with open(subname,'w') as f:
        f.write(f"""#!/bin/bash
#SBATCH --time=48:00:00                  # Job run time (hh:mm:ss)
#SBATCH --nodes=1                        # Number of nodes
#SBATCH --cpus-per-task={ncores}             # Number of task (cores/ppn) per node
#SBATCH --job-name={jobname}            # Name of batch job
#SBATCH --partition={queue}           # Partition (queue)
#SBATCH --output=outputs/{jobname}.o
##SBATCH --error=outputs/{jobname}.e              # Name of batch job error file
##SBATCH --mail-user=lkwagner@illinois.edu  # Send email notifications
##SBATCH --mail-type=BEGIN,END           # Type of email notifications to send
. ~/bin/activate_conda.sh
conda activate forge3.11
export OMP_NUM_THREADS=1
srun -n 1 -c {ncores} python3  dmcrun.py {args} >& outputs/{jobname}.stdout
    """)

    os.system(f"sbatch {subname}")
    os.remove(subname)

def should_submit(fname, tau, branchtime=5):
    if not os.path.isfile(fname):
        return True
    warmup=int(10/(tau*branchtime))
    nreblock = 30
    data = pyq.read_mc_output(fname,warmup=warmup, reblock=nreblock)
    err = data['energytotal_err']
    #print(fname, err)
    if err > 5e-5:
        print(fname, err)
        return True
    return False



if __name__=="__main__":
    for directory in ['m','w','m---w','mw']:
        for tau in [.10, .08, .04, .02, .01, .005, .0025]:
            for localization in ['DLA','LA','tmoves']:
                fname = f"{directory}/{localization}_j3_third_10_2000_{tau}_1.0_5.hdf5"
                if should_submit(fname, tau):
                    print("should submit ", fname)
                    submit_dmc(directory=directory, tstep=tau, localization=localization, branchtime=5,npartitions=ncores, wavefunction='j3_third')
