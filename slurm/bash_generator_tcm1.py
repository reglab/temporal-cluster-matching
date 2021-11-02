import os
import sys

def put_qmark(s):
    s = "\"" + s +"\""
    return s


def generate(dataset_path, dataset_name, cluster, buffer, array, alg):
    dataset_list = []
    cluster_list = []
    buffer_list = []
    output_dir_list = []
    alg_list = []
    for c in cluster:
        for b in buffer:
            for a in alg:
                fn = dataset_path + dataset_name + '.geojson'
                dataset_list.append(fn)
                cluster_list.append(c)
                buffer_list.append(b)
                output_dir = '../all_buildings/data/output/compare_models/' + dataset_name + '_' + str(c) + '_' + str(b) + '/'
                output_dir_list.append(output_dir)
                alg_list.append(a)


    S = "#!/bin/bash\n"
    S += "#SBATCH --begin=now\n"
    S += "#SBATCH --job-name=tcm\n"
    S += "#SBATCH --ntasks=1\n"
    # S += "#SBATCH --output=tcm_res.txt\n"
    S += "#SBATCH --mail-type=ALL\n"
    S += "#SBATCH --mail-user=nathanjo@law.stanford.edu\n"
    S += "#SBATCH --partition=owners\n"
    S += "#SBATCH --mem=4GB\n"
    S += "#SBATCH --time=6:00:00\n"
    S += "#SBATCH --array=0-"
    S += str(array)

    S += "\n"
    S += "\n"

    S += "cd ../"

    S += "\n"
    S += "\n"

    S += "dataset_list=" + put_qmark(" ".join(str(item) for item in dataset_list) + "\n")
    S += "\n"
    S += "cluster_list=" + put_qmark(" ".join(str(item) for item in cluster_list) + "\n")
    S += "\n"
    S += "buffer_list=" + put_qmark(" ".join(str(item) for item in buffer_list) + "\n")
    S += "\n"
    S += "output_dir_list=" + put_qmark(" ".join(str(item) for item in output_dir_list) + "\n")
    S += "\n"
    S += "alg_list=" + put_qmark(" ".join(str(item) for item in alg_list) + "\n")
    S += "\n"
    S += 'dataset_list=($dataset_list)' + "\n"
    S += 'cluster_list=($cluster_list)' + "\n"
    S += 'buffer_list=($buffer_list)' + "\n"
    S += 'output_dir_list=($output_dir_list)' + "\n"
    S += 'alg_list=($alg_list)' + "\n"

    S += "\n"
    S += "\n"
    command = 'singularity exec $GROUP_HOME/singularity/cafo_permit+tcm_10-21-21.sif python run_algorithm1.py --dataset ' + \
              '${dataset_list[$SLURM_ARRAY_TASK_ID]}' + ' --num_clusters ' + '${cluster_list[$SLURM_ARRAY_TASK_ID]}' + \
              ' --buffer ' + '${buffer_list[$SLURM_ARRAY_TASK_ID]}' + ' --output_dir ' + '${output_dir_list[$SLURM_ARRAY_TASK_ID]}' + \
              ' --algorithm ' + '${alg_list[$SLURM_ARRAY_TASK_ID]}'
    S += command
    S += "\n"

    slurm_file = 'slurm_' + dataset_name + ".sh"
    f = open(slurm_file, "w+")
    f.write(S)
    f.close()
    # print(slurm_file)


def main():
    dataset_path = '../all_buildings/data/input/compare_models/'
    dataset_name = ['miami', 'orlando', 'polk_rural', 'polk_semi']
    for i in dataset_name:
        cluster = [16, 32]
        buffer = [0.001, 0.0005, 0.0001]
        alg = ['kl']
        array = (len(cluster) * len(buffer) * len(alg)) - 1

        generate(dataset_path, i, cluster, buffer, array, alg)

if __name__ == "__main__":
    main()