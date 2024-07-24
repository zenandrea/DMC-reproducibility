# Orca directories
export PATH=$HOME/Software/openmpi-4.1.1/bin:$PATH
export LD_LIBRARY_PATH=$HOME/Software/openmpi-4.1.1/lib:$LD_LIBRARY_PATH
ORCA_DIR="/home/matteo/Software/orca.5.0.3"
ORCA_EXE=${ORCA_DIR}"/orca"


# Input / output orca run
INPUT=$1.inp
OUTPUT=$1.out

# Orca Job
  date
      time ${ORCA_EXE} ${INPUT} > ${OUTPUT}
  date




