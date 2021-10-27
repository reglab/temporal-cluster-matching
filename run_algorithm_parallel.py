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

def driver(index, geom):
    data_images, masks, years = dataloader_global.get_data_stack_from_geom(geom, buffer=args_global.buffer)

    if args_global.algorithm == "kl":
        divergence_values = algorithms.calculate_change_values(data_images, masks, n_clusters=args_global.num_clusters)
    elif args_global.algorithm == "color":
        divergence_values = algorithms.calculate_change_values_with_color(data_images, masks)

    with open(output_fn, "a") as f:
        f.write("%d," % (index))
        for year in years:
            f.write("%d," % (year))
        f.write("|,")
        for divergence in divergence_values:
            f.write("%0.4f," % (divergence))
        f.write("\n")

def make_global(dataloader, args):
    global dataloader_global
    global args_global

    dataloader_global = dataloader
    args_global = args

def main():
    start_time = time.time()
    print("Starting algorithm at %s" % (str(datetime.datetime.now())))

    ##############################
    # Ensure output directory exists; if a CSV exists already, indicate code to pick up where we left off
    ##############################
    index_done = []
    if os.path.exists(args.output_dir):
        # see if csv exists within directory
        if os.path.exists(os.path.join(args.output_dir, "results.csv")):
            results = pd.read_csv(os.path.join(args.output_dir, "results.csv"))
            index_done = results.iloc[:, 0].tolist()
            index_done = [int(i) for i in index_done]
    else:
        os.makedirs(args.output_dir, exist_ok=False)

    output_fn = os.path.join(
        args.output_dir,
        "results.csv"
    )

    ##############################
    # Load geoms / create dataloader
    ##############################
    geoms = utils.get_all_geoms_from_file1(os.path.join("./data/", args.dataset), index_done)
    dataloader = DataInterface.NAIPDataLoader()
    if args.buffer is not None and args.buffer > 1:
        print("WARNING: your buffer distance is probably set incorrectly, this should be in units of degrees (at equator, more/less)")

    nprocs = mp.cpu_count()
    p = mp.Pool(processes=nprocs, initializer=make_global, initargs=(dataloader, args,))
    p.starmap(driver, geoms)

    ##############################
    # Loop through geoms and run
    ##############################


if __name__ == "__main__":
    main()