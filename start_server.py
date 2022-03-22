from multiprocessing.managers import BaseManager
from rtree import Rtree
import rtree

class RtreeManager(BaseManager):
    pass

##############################
# Trying out multiprocessing RTree
##############################

RtreeManager.register('add')
RtreeManager.register('intersection')

if __name__ == '__main__':
    class NoisyRtree(Rtree):
        def add(self, i, bbox):
            Rtree.add(self, i, bbox)

        def intersection(self, bbox):
            return Rtree.intersection(self, bbox)


    index = NoisyRtree("tiles/tile_index")

    RtreeManager.register('add', index.add)
    RtreeManager.register('intersection', index.intersection)

    manager = RtreeManager(address=('', 50000), authkey=b'')
    server = manager.get_server()
    print('Server started')
    with open('log.txt', 'a') as f:
        f.write("Server started\n")

    server.serve_forever()