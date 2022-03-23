import start_server

import time
import datetime
import multiprocessing as mp
# from temporal_cluster_matching import utils, DataInterface
start_time = time.time()
print("Starting algorithm at %s" % (str(datetime.datetime.now())))

##############################
# Ensure output directory exists; if a CSV exists already, indicate code to pick up where we left off
##############################
# index_done = []
# if os.path.exists(args.output_dir):
#     # see if csv exists within directory
#     if os.path.exists(os.path.join(args.output_dir, "results.csv")):
#         results = pd.read_csv(os.path.join(args.output_dir, "results.csv"))
#         index_done = results.iloc[:, 0].tolist()
#         index_done = [str(i) for i in index_done]
# else:
#     os.makedirs(args.output_dir, exist_ok=False)
#
# output_fn = os.path.join(
#     args.output_dir,
#     "results.csv"
# )

##############################
# Load geoms / create dataloader
##############################
# if not os.path.exists(args.dataset):
#     print("Dataset doesn't exist. It's likely that there just aren't any structures in this county.")
#     return

# geoms = utils.get_all_geoms_from_file1('../all_buildings/data/input/OSM/san_jose_test.geojson', [])
# dataloader = DataInterface.NAIPDataLoader()

manager = start_server.RtreeManager(address=('localhost', 50000), authkey=b'')
manager.connect()

# manager = rtree.index.Index('tiles/tile_index')

nprocs = mp.cpu_count()
print(nprocs)

result = manager.intersection((-121.9397863207285, 37.36443486181571, -121.9397863207285, 37.36443486181571))
# print(type(result))
print(result)