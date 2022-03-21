#!/bin/bash
#SBATCH --begin=now
#SBATCH --job-name=tcm
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nathanjo@law.stanford.edu
#SBATCH --partition=owners
#SBATCH --time=00:30:00
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=4GB 

cd ../

singularity exec $GROUP_HOME/singularity/cafo_permit+tcm_10-21-21.sif python run_algorithm_parallel.py --dataset "../all_buildings/data/input/OSM/san_jose_test.geojson" --num_clusters 32 --buffer 0.0001 --output_dir ../all_buildings/data/output/san_jose/32_0.0001

