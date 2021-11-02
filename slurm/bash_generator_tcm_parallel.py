import os
import sys

def put_qmark(s):
    s = "\"" + s +"\""
    return s


def generate(dataset_type, county, cluster, buffer, array, alg):

    dataset_list = []
    cluster_list = []
    buffer_list = []
    output_dir_list = []
    alg_list = []
    for t in dataset_type:
        for co in county:
            for c in cluster:
                for b in buffer:
                    for a in alg:
                        dataset_name = t + '/' + co + '_footprints.geojson'
                        dataset_list.append(dataset_name)
                        cluster_list.append(c)
                        buffer_list.append(b)
                        output_dir = 'results/kl/' + co + '_' + t + '_' + str(c) + '_' + str(b) + '/'
                        output_dir_list.append(output_dir)
                        alg_list.append(a)


    S = "#!/bin/bash\n"
    S += "#SBATCH --begin=now\n"
    S += "#SBATCH --job-name=tcm\n"
    S += "#SBATCH --ntasks=1\n"
    S += "#SBATCH --output=tcm_res.txt\n"
    S += "#SBATCH --mail-type=ALL\n"
    S += "#SBATCH --mail-user=nathanjo@law.stanford.edu\n"
    S += "#SBATCH --partition=owners\n"
    S += "#SBATCH --mem-per-cpu=2GB\n"
    S += "#SBATCH --cpus-per-task=8\n"
    S += "#SBATCH --time=03:00:00\n"
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
    command = 'singularity exec $GROUP_HOME/singularity/cafo_permit+tcm_10-21-21.sif python run_algorithm_parallel.py --dataset ' + \
              '${dataset_list[$SLURM_ARRAY_TASK_ID]}' + ' --num_clusters ' + '${cluster_list[$SLURM_ARRAY_TASK_ID]}' + \
              ' --buffer ' + '${buffer_list[$SLURM_ARRAY_TASK_ID]}' + ' --output_dir ' + '${output_dir_list[$SLURM_ARRAY_TASK_ID]}' + \
              ' --algorithm ' + '${alg_list[$SLURM_ARRAY_TASK_ID]}'
    S += command
    S += "\n"

    slurm_file = 'slurm_' + county[0] + "_parallel.sh"
    f = open(slurm_file, "w+")
    f.write(S)
    f.close()
    # print(slurm_file)


def main():
    county = ['Flagler', 'Lee', 'Bay', 'Putnam', 'Jefferson', 'Lafayette',
       'Hamilton', 'Levy', 'Polk', 'St. Lucie', 'Okaloosa', 'Columbia',
       'Holmes', 'Collier', 'Baker', 'Sarasota', 'Suwannee', 'Taylor',
       'Union', 'Clay', 'Madison', 'Osceola', 'Marion', 'Jackson',
       'Alachua', 'Hardee', 'Nassau', 'Washington', 'Santa Rosa',
       'Brevard', 'Liberty', 'Indian River', 'Gadsden', 'Gulf', 'Leon',
       'Hillsborough', 'Charlotte', 'Hernando', 'Wakulla', 'Walton',
       'Volusia', 'Hendry', 'Orange', 'Broward', 'Palm Beach',
       'Gilchrist', 'Miami-Dade', 'Highlands', 'Citrus', 'Okeechobee',
       'St. Johns', 'DeSoto', 'Glades', 'Manatee', 'Calhoun', 'Lake',
       'Pinellas', 'Franklin', 'Pasco', 'Sumter', 'Seminole', 'Bradford',
       'Duval', 'Martin', 'Dixie', 'Escambia', 'Monroe']

    county = ['Broward']

    dataset_type = ['rural']
    # i guess there's no need to do very_rural because it's just a subset of rural--we can track using the index
    cluster = [16, 32]
    buffer = [0.001, 0.0005, 0.0001]
    alg = ['kl']
    array = (len(county) * len(cluster) * len(buffer) * len(alg) * len(dataset_type)) - 1

    generate(dataset_type, county, cluster, buffer, array, alg)

if __name__ == "__main__":
    main()