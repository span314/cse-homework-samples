#!/bin/bash
#SBATCH -p seas_iacs
#SBATCH -J matrixmultiplication
#SBATCH -n 8
#SBATCH -N 1
#SBATCH -t 0-2:00
#SBATCH --mem 64000
#SBATCH -o mm%j_%N.out
#SBATCH -e mm%j_%N.err

#Echo Commands
set -x

#Set Num Threads
export OMP_NUM_THREADS=8

#Load Modules
source new-modules.sh
module load legacy/0.0.1-fasrc01
module load centos6/cython-0.20_python-3.3.2
module load gcc/5.2.0-fasrc02
module load python/3.4.1-fasrc01

#Run Python Script
python problem4.py