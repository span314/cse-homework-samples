#!/bin/bash
#SBATCH -p seas_iacs
#SBATCH -J h5p1
#SBATCH -n 2
#SBATCH -N 1
#SBATCH -t 0-4:00
#SBATCH --mem 16000
#SBATCH -o h5p1%j_%N.out
#SBATCH -e h5p1%j_%N.err

#Echo Commands
set -x

#Load Modules
source new-modules.sh
module load R/3.3.3-fasrc01

#Run script
R CMD BATCH prob1.R
