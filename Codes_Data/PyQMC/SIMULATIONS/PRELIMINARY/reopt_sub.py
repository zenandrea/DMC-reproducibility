#!/usr/bin/env python3
import sys
import uuid
import os

def submit(directory):
    subname = "sub" + str(uuid.uuid4())
    jobname=f"opt{directory}"
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
srun -n 1 -c 40 python3  reopt_single.py {directory} >& outputs/{jobname}.stdout
    """)

    os.system(f"sbatch {subname}")


if __name__=="__main__":
    for directory in ['m','w', 'm---w', 'mw']:
        submit(directory)
