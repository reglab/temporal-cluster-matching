from multiprocessing.managers import BaseManager

class RtreeManager(BaseManager):
    pass

RtreeManager.register('add')
RtreeManager.register('intersection')

if __name__ == '__main__':

    from rtree.index import Rtree


    class NoisyRtree():
        def __init__(self, rtree):
            self.rtree = rtree

        def add(self, i, bbox):
            self.rtree.add(i, bbox)

        def intersection(self, bbox):
            return list(self.rtree.intersection(bbox))

    index = NoisyRtree(Rtree('tiles/tile_index'))

    RtreeManager.register('add', index.add)
    RtreeManager.register('intersection', index.intersection)

    manager = RtreeManager(address=('', 50000), authkey=b'')
    server = manager.get_server()
    print("Server started")
    server.serve_forever()