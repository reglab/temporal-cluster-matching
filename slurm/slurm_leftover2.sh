#!/bin/bash
#SBATCH --begin=now
#SBATCH --job-name=tcm
#SBATCH --ntasks=1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nathanjo@law.stanford.edu
#SBATCH --partition=owners
#SBATCH --mem=4GB
#SBATCH --time=6:00:00
#SBATCH --array=0-2

cd ../

dataset_list="../all_buildings/data/input/compare_models/orlando.geojson ../all_buildings/data/input/compare_models/miami.geojson ../all_buildings/data/input/compare_models/miami.geojson
"
cluster_list="32 16 32
"
buffer_list="0.001 0.001 0.001
"
output_dir_list="../all_buildings/data/output/compare_models/orlando_32_0.001/ ../all_buildings/data/output/compare_models/miami_16_0.001/ ../all_buildings/data/output/compare_models/miami_32_0.001/
"
alg_list="kl kl kl
"
dataset_list=($dataset_list)
cluster_list=($cluster_list)
buffer_list=($buffer_list)
output_dir_list=($output_dir_list)
alg_list=($alg_list)


singularity exec $GROUP_HOME/singularity/cafo_permit+tcm_10-21-21.sif python run_algorithm1.py --dataset ${dataset_list[$SLURM_ARRAY_TASK_ID]} --num_clusters ${cluster_list[$SLURM_ARRAY_TASK_ID]} --buffer ${buffer_list[$SLURM_ARRAY_TASK_ID]} --output_dir ${output_dir_list[$SLURM_ARRAY_TASK_ID]} --algorithm ${alg_list[$SLURM_ARRAY_TASK_ID]}
