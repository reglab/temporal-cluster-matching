#!/bin/bash
#SBATCH --begin=now
#SBATCH --job-name=tcm
#SBATCH --ntasks=1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nathanjo@law.stanford.edu
#SBATCH --partition=owners
#SBATCH --mem=4GB
#SBATCH --time=3:00:00
#SBATCH --array=0-5

cd ../

dataset_list="../all_buildings/data/input/compare_models/polk_semi.geojson ../all_buildings/data/input/compare_models/polk_semi.geojson ../all_buildings/data/input/compare_models/polk_semi.geojson ../all_buildings/data/input/compare_models/polk_semi.geojson ../all_buildings/data/input/compare_models/polk_semi.geojson ../all_buildings/data/input/compare_models/polk_semi.geojson
"
cluster_list="16 16 16 32 32 32
"
buffer_list="0.001 0.0005 0.0001 0.001 0.0005 0.0001
"
output_dir_list="../all_buildings/data/output/compare_models/polk_semi_16_0.001/ ../all_buildings/data/output/compare_models/polk_semi_16_0.0005/ ../all_buildings/data/output/compare_models/polk_semi_16_0.0001/ ../all_buildings/data/output/compare_models/polk_semi_32_0.001/ ../all_buildings/data/output/compare_models/polk_semi_32_0.0005/ ../all_buildings/data/output/compare_models/polk_semi_32_0.0001/
"
alg_list="kl kl kl kl kl kl
"
dataset_list=($dataset_list)
cluster_list=($cluster_list)
buffer_list=($buffer_list)
output_dir_list=($output_dir_list)
alg_list=($alg_list)


singularity exec $GROUP_HOME/singularity/cafo_permit+tcm_10-21-21.sif python run_algorithm1.py --dataset ${dataset_list[$SLURM_ARRAY_TASK_ID]} --num_clusters ${cluster_list[$SLURM_ARRAY_TASK_ID]} --buffer ${buffer_list[$SLURM_ARRAY_TASK_ID]} --output_dir ${output_dir_list[$SLURM_ARRAY_TASK_ID]} --algorithm ${alg_list[$SLURM_ARRAY_TASK_ID]}
