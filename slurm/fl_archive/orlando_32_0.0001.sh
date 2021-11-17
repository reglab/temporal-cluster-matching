#!/bin/bash
#SBATCH --begin=now
#SBATCH --job-name=tcm
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nathanjo@law.stanford.edu
#SBATCH --partition=owners
#SBATCH --time=3:00:00
#SBATCH --mem=4GB 

cd ../

singularity exec $GROUP_HOME/singularity/cafo_permit+tcm_10-21-21.sif python run_algorithm1.py --dataset "../all_buildings/data/input/compare_models/orlando_parcel.geojson" --num_clusters 32 --buffer 0.0001 --output_dir ../all_buildings/data/output/compare_models/orlando_32_0.0001_parcel/ --algorithm kl --parcel_type parcel
