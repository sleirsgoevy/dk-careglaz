import bottle, os.path, sys
from .app import the_app

for i in range(len(sys.path)):
    sys.path[i] = os.path.realpath(sys.path[i])

os.chdir('data')

bottle.run(the_app, host='')
