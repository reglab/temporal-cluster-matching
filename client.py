import start_server
manager = start_server.RtreeManager(address=('', 50000), authkey=b'')
manager.connect()
# print(manager.expose())
result = manager.intersection((-121.9397863207285, 37.36443486181571, -121.9397863207285, 37.36443486181571))
# print(type(result))
print(result)