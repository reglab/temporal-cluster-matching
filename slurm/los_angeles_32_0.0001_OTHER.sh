#!/bin/bash
#SBATCH --begin=now
#SBATCH --job-name=tcm
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nathanjo@law.stanford.edu
#SBATCH --partition=owners
#SBATCH --time=2:00:00
#SBATCH --mem=64GB 

cd ../

singularity exec $GROUP_HOME/singularity/cafo_permit+tcm_10-21-21.sif python run_algorithm1.py --dataset "../all_buildings/data/input/los_angeles/tcm_other.geojson" --num_clusters 32 --buffer 0.0001 --output_dir ../all_buildings/data/output/los_angeles/other/32_0.0001 --algorithm kl

