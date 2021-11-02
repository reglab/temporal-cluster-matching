#!/bin/bash
#SBATCH --begin=now
#SBATCH --job-name=tcm
#SBATCH --ntasks=1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nathanjo@law.stanford.edu
#SBATCH --partition=owners
#SBATCH --mem=4GB
#SBATCH --time=10:00:00
#SBATCH --array=0-29

cd ../

dataset_list="rural/Flagler_footprints.geojson rural/Flagler_footprints.geojson rural/Flagler_footprints.geojson rural/Flagler_footprints.geojson rural/Flagler_footprints.geojson rural/Flagler_footprints.geojson rural/Lee_footprints.geojson rural/Lee_footprints.geojson rural/Lee_footprints.geojson rural/Lee_footprints.geojson rural/Lee_footprints.geojson rural/Lee_footprints.geojson rural/Bay_footprints.geojson rural/Bay_footprints.geojson rural/Bay_footprints.geojson rural/Bay_footprints.geojson rural/Bay_footprints.geojson rural/Bay_footprints.geojson rural/Putnam_footprints.geojson rural/Putnam_footprints.geojson rural/Putnam_footprints.geojson rural/Putnam_footprints.geojson rural/Putnam_footprints.geojson rural/Putnam_footprints.geojson rural/Jefferson_footprints.geojson rural/Jefferson_footprints.geojson rural/Jefferson_footprints.geojson rural/Jefferson_footprints.geojson rural/Jefferson_footprints.geojson rural/Jefferson_footprints.geojson
"
cluster_list="16 16 16 32 32 32 16 16 16 32 32 32 16 16 16 32 32 32 16 16 16 32 32 32 16 16 16 32 32 32
"
buffer_list="0.001 0.0005 0.0001 0.001 0.0005 0.0001 0.001 0.0005 0.0001 0.001 0.0005 0.0001 0.001 0.0005 0.0001 0.001 0.0005 0.0001 0.001 0.0005 0.0001 0.001 0.0005 0.0001 0.001 0.0005 0.0001 0.001 0.0005 0.0001
"
output_dir_list="results/kl/Flagler_rural_16_0.001/ results/kl/Flagler_rural_16_0.0005/ results/kl/Flagler_rural_16_0.0001/ results/kl/Flagler_rural_32_0.001/ results/kl/Flagler_rural_32_0.0005/ results/kl/Flagler_rural_32_0.0001/ results/kl/Lee_rural_16_0.001/ results/kl/Lee_rural_16_0.0005/ results/kl/Lee_rural_16_0.0001/ results/kl/Lee_rural_32_0.001/ results/kl/Lee_rural_32_0.0005/ results/kl/Lee_rural_32_0.0001/ results/kl/Bay_rural_16_0.001/ results/kl/Bay_rural_16_0.0005/ results/kl/Bay_rural_16_0.0001/ results/kl/Bay_rural_32_0.001/ results/kl/Bay_rural_32_0.0005/ results/kl/Bay_rural_32_0.0001/ results/kl/Putnam_rural_16_0.001/ results/kl/Putnam_rural_16_0.0005/ results/kl/Putnam_rural_16_0.0001/ results/kl/Putnam_rural_32_0.001/ results/kl/Putnam_rural_32_0.0005/ results/kl/Putnam_rural_32_0.0001/ results/kl/Jefferson_rural_16_0.001/ results/kl/Jefferson_rural_16_0.0005/ results/kl/Jefferson_rural_16_0.0001/ results/kl/Jefferson_rural_32_0.001/ results/kl/Jefferson_rural_32_0.0005/ results/kl/Jefferson_rural_32_0.0001/
"
alg_list="kl kl kl kl kl kl kl kl kl kl kl kl kl kl kl kl kl kl kl kl kl kl kl kl kl kl kl kl kl kl
"
dataset_list=($dataset_list)
cluster_list=($cluster_list)
buffer_list=($buffer_list)
output_dir_list=($output_dir_list)
alg_list=($alg_list)


singularity exec $GROUP_HOME/singularity/cafo_permit+tcm_10-21-21.sif python run_algorithm1.py --dataset ${dataset_list[$SLURM_ARRAY_TASK_ID]} --num_clusters ${cluster_list[$SLURM_ARRAY_TASK_ID]} --buffer ${buffer_list[$SLURM_ARRAY_TASK_ID]} --output_dir ${output_dir_list[$SLURM_ARRAY_TASK_ID]} --algorithm ${alg_list[$SLURM_ARRAY_TASK_ID]}
