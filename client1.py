import start_server

manager = start_server.RtreeManager(address=('localhost', 50000), authkey=b'')
manager.connect()
with open('test.txt', 'a') as f:
    f.write('starting... ')

result = manager.intersection((-121.9397863207285, 37.36443486181571, -121.9397863207285, 37.36443486181571))
# print(type(result))
print(result)