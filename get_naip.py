from temporal_cluster_matching import utils, DataInterface, algorithms
import imageio
import pandas as pd
from fiona.transform import transform
from shapely.geometry import Point, mapping, box

def pull_imagery(geom, tag='cafo'):
    rgb_images, years = dataloader.get_rgb_stack_from_geom(geom, buffer=0.003,
                                                           show_outline=False,
                                                           geom_crs="EPSG:4326")
    for im, year in zip(rgb_images, years):
        out_file = f'data/{tag}_{year}.tif'
        imageio.imwrite(out_file, im)

dataloader = DataInterface.NAIPDataLoader()

print("pulling NAIP imagery")
list_of_areas = {'miami': box(-80.34919799550399, 25.627390848851284, -80.3767718790555, 25.614003509369763),
                 'orlando': box(-81.33914527918063, 28.505168467284232, -81.37053012436698, 28.495222825819365),
                 'polk_semi': box( -81.5771979853621, 27.890333280245404, -81.59352547707883, 27.88299148172118),
                 'polk_rural': box(-81.49858184918745, 27.841193739214805, -81.52030806885028, 27.821246638518986)}

for area, geom in list_of_areas.items():
    pull_imagery(geom, tag=area)
