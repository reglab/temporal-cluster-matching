'''
Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the MIT License.
'''
import os
import time
import datetime
import argparse
import pandas as pd

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

parser.add_argument('--parcel_type', required=False, default='no_parcel',
                    choices = ('no_parcel', 'parcel', 'parcel_dedup'),
                    help='Specify if using parcel type, dedup, etc.',)

parser.add_argument('--superres', requires=True, choices=('yes', 'no'))

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--buffer', type=float, help='Amount to buffer for defining a neighborhood. Note: this will be in terms of units of the dataset.')

parser.add_argument('--output_dir', type=str, required=True, help='Path to an empty directory where outputs will be saved. This directory will be created if it does not exist.')
parser.add_argument('--verbose', action="store_true", default=False, help='Enable training with feature disentanglement')
parser.add_argument('--overwrite', action='store_true', default=False, help='Ignore checking whether the output directory has existing data')

args = parser.parse_args()


def main():
    start_time = time.time()
    print("Algorithm: {}, {}, {}".format(args.dataset, str(args.buffer), str(args.num_clusters)))
    print("Starting algorithm at %s" % (str(datetime.datetime.now())))

    ##############################
    # Ensure output directory exists; if a CSV exists already, indicate code to pick up where we left off
    ##############################
    index_done = []
    if os.path.exists(args.output_dir):
        # see if csv exists within directory
        if os.path.exists(os.path.join(args.output_dir, "results.csv")):
            results = pd.read_csv(os.path.join(args.output_dir, "results.csv"))
            if args.parcel_type == 'parcel_dedup':
                index_done = results.iloc[:, 0].tolist()
                index_done = [i for i in index_done]
            else:
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
    if not os.path.exists(args.dataset):
        print("Dataset doesn't exist. It's likely that there just aren't any structures in this county.")
        return

    # geoms = utils.get_all_geoms_from_file1(os.path.join("./data/", args.dataset), index_done)
    if args.parcel_type == 'no_parcel':
        geoms = utils.get_all_geoms_from_file1(args.dataset, index_done)
    elif args.parcel_type == 'parcel':
        geoms = utils.get_all_geoms_from_file_parcel(args.dataset, index_done)

    dataloader = DataInterface.NAIPDataLoader()
    if args.buffer is not None and args.buffer > 1:
        print("WARNING: your buffer distance is probably set incorrectly, this should be in units of degrees (at equator, more/less)")

    ##############################
    # Loop through geoms and run
    ##############################
    tic = time.time()
    count = 0
    for i in geoms:
        if count % 10000 == 0:
            print("%d/%d\t%0.2f seconds" % (count, len(geoms), time.time() - tic))
            tic = time.time()

        if args.superres == 'yes':
            data_images, masks, years = dataloader.get_data_stack_from_geom_superres(i, parcel=False, buffer=args.buffer, geom_crs="epsg:4326")
        else:
            data_images, masks, years = dataloader.get_data_stack_from_geom(i, parcel=False, buffer=args.buffer,
                                                                            geom_crs="epsg:4326")

        if args.algorithm == "kl":
            divergence_values = algorithms.calculate_change_values(i[0], years, data_images, masks, n_clusters=args.num_clusters)
        elif args.algorithm == "color":
            divergence_values = algorithms.calculate_change_values_with_color(data_images, masks)

        with open(output_fn, "a") as f:
            f.write("%d," % (int(i[0])))
            for year in years:
                f.write("%d," % (year))
            f.write("|,")
            for divergence in divergence_values:
                f.write("%0.4f," % (divergence))
            f.write("\n")

        count += 1


    print("Finished in %0.2f seconds" % (time.time() - start_time))

if __name__ == "__main__":
    main()