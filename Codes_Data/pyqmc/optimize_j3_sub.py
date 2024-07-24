#!/usr/bin/env python3
import sys
import uuid
import os

partition = "qmchamm"
npartitions=40
def submit(directory):
    subname = "outputs/sub" + str(uuid.uuid4())
    jobname=f"optj3{directory}"
    with open(subname,'w') as f:
        f.write(f"""#!/bin/bash
#SBATCH --time=36:00:00                  # Job run time (hh:mm:ss)
#SBATCH --nodes=1                        # Number of nodes
#SBATCH --cpus-per-task={npartitions}            # Number of task (cores/ppn) per node
#SBATCH --job-name={jobname}            # Name of batch job
#SBATCH --partition={partition}           # Partition (queue)
#SBATCH --output=outputs/{jobname}.o
##SBATCH --error=outputs/{jobname}.e              # Name of batch job error file
##SBATCH --mail-user=lkwagner@illinois.edu  # Send email notifications
##SBATCH --mail-type=BEGIN,END           # Type of email notifications to send
. ~/bin/activate_conda.sh
export OMP_NUM_THREADS=1
srun -n 1 -c {npartitions} python3  optimize_j3.py {directory} >& outputs/{jobname}.stdout
    """)

    os.system(f"sbatch {subname}")


if __name__=="__main__":
    for directory in ['m---w']:
        submit(directory)
