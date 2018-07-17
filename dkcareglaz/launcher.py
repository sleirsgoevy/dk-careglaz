import bottle, os.path, sys

for i in range(len(sys.path)):
    sys.path[i] = os.path.realpath(sys.path[i])

os.chdir('data')

bottle.run(host='')
