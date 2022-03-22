'''
Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the MIT License.
'''
import os
import time
import datetime
import argparse
import pandas as pd
import multiprocessing as mp

from . import start_server
from temporal_cluster_matching import utils, DataInterface, algorithms

parser = argparse.ArgumentParser(description='Script for running temporal cluster matching')
parser.add_argument('--dataset', required=True,
    help='Dataset to use'
)
parser.add_argument('--algorithm', default='kl',
    choices=(
        'kl',
        'color'
    ),
    help='Algorithm to use'
)

parser.add_argument('--num_clusters', type=int, required=False, help='Number of clusters to use in k-means step.')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--buffer', type=float, help='Amount to buffer for defining a neighborhood. Note: this will be in terms of units of the dataset.')

parser.add_argument('--output_dir', type=str, required=True, help='Path to an empty directory where outputs will be saved. This directory will be created if it does not exist.')
parser.add_argument('--verbose', action="store_true", default=False, help='Enable training with feature disentanglement')
parser.add_argument('--overwrite', action='store_true', default=False, help='Ignore checking whether the output directory has existing data')

args = parser.parse_args()


def driver(index, geom, manager):
    data_images, masks, years = dataloader_global.get_data_stack_from_geom((index, geom), False, args_global.buffer, manager)

    if args_global.algorithm == "kl":
        divergence_values = algorithms.calculate_change_values(data_images, masks, n_clusters=args_global.num_clusters)
    elif args_global.algorithm == "color":
        divergence_values = algorithms.calculate_change_values_with_color(data_images, masks)

    with open(output_fn_global, "a") as f:
        f.write("%d," % (index))
        for year in years:
            f.write("%d," % (year))
        f.write("|,")
        for divergence in divergence_values:
            f.write("%0.4f," % (divergence))
        f.write("\n")

def make_global(dataloader, args, output_fn):
    global dataloader_global
    global args_global
    global output_fn_global

    dataloader_global = dataloader
    args_global = args
    output_fn_global = output_fn

def main():
    start_time = time.time()
    print("Starting algorithm at %s" % (str(datetime.datetime.now())))
    with open('log.txt', 'a') as f:
        f.write("Starting algorithm at %s\n" % (str(datetime.datetime.now())))

    ##############################
    # Ensure output directory exists; if a CSV exists already, indicate code to pick up where we left off
    ##############################
    index_done = []
    if os.path.exists(args.output_dir):
        # see if csv exists within directory
        if os.path.exists(os.path.join(args.output_dir, "results.csv")):
            results = pd.read_csv(os.path.join(args.output_dir, "results.csv"))
            index_done = results.iloc[:, 0].tolist()
            index_done = [str(i) for i in index_done]
    else:
        os.makedirs(args.output_dir, exist_ok=False)

    output_fn = os.path.join(
        args.output_dir,
        "results.csv"
    )

    ##############################
    # Load geoms / create dataloader
    ##############################
    if not os.path.exists(args.dataset):
        print("Dataset doesn't exist. It's likely that there just aren't any structures in this county.")
        return

    geoms = utils.get_all_geoms_from_file1(args.dataset, index_done)
    dataloader = DataInterface.NAIPDataLoader()
    if args.buffer is not None and args.buffer > 1:
        print("WARNING: your buffer distance is probably set incorrectly, this should be in units of degrees (at equator, more/less)")

    manager = start_server.RtreeManager(address=('', 50000), authkey=b'')
    manager.connect()

    nprocs = mp.cpu_count()
    print(nprocs)
    with open('log.txt', 'a') as f:
        f.write(f"# CPUs: {nprocs}\n")
    p = mp.Pool(processes=nprocs, initializer=make_global, initargs=(dataloader, args, output_fn,))

    p.starmap(driver, geoms, manager)

    ##############################
    # Loop through geoms and run
    ##############################


if __name__ == "__main__":
    main()