#!/usr/bin/env python3
import sys
import uuid
import os

def submit_dmc(directory, tau):
    subname = str(uuid.uuid4())
    jobname=f"{directory}_{tau}"
    with open(subname,'w') as f:
        f.write(f"""#!/bin/bash
#SBATCH --time=36:00:00                  # Job run time (hh:mm:ss)
#SBATCH --nodes=1                        # Number of nodes
#SBATCH --cpus-per-task=40             # Number of task (cores/ppn) per node
#SBATCH --job-name={jobname}            # Name of batch job
#SBATCH --partition=qmchamm           # Partition (queue)
#SBATCH --output=outputs/{jobname}.o
##SBATCH --error=outputs/{jobname}.e              # Name of batch job error file
##SBATCH --mail-user=lkwagner@illinois.edu  # Send email notifications
##SBATCH --mail-type=BEGIN,END           # Type of email notifications to send
. ~/bin/activate_conda.sh
export OMP_NUM_THREADS=1
srun -n 1 -c 40 python3  dmc_opt2.py {directory} {tau} >& outputs/{jobname}.stdout
    """)

    os.system(f"sbatch {subname}")


if __name__=="__main__":
    for directory in ['m','w','mw','m---w']:
        for tau in [0.08,0.04,0.02,0.01]:
            submit_dmc(directory, tau)
