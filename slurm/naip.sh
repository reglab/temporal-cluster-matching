#!/bin/bash
#SBATCH --begin=now
#SBATCH --job-name=naip
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nathanjo@law.stanford.edu
#SBATCH --partition=owners
#SBATCH --time=1:00:00
#SBATCH --mem=4GB 

cd ../

singularity exec $GROUP_HOME/singularity/cafo_permit+tcm_10-21-21.sif python get_naip.py

