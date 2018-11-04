from .app import the_app
from bottle import static_file, response
from os.path import isfile, sep as pathsep, split as pathsplit

def file(path, error=200, kick=False):
    if kick:
        response.set_cookie('credentials', 'invalid')
    response.status = error
    return static_file(path, pathsplit(__path__[0])[0])

@the_app.route('/theory/<name>')
def theory(name):
    if pathsep in name or not isfile('tasksheets/'+name+'/theory.html'):
        return file("forbidden.html", 403)
#       response.status = 403
#       return '<html><head><title>Теория</title></head><body><h3>'\
#              'Замечание для умных</h3><p>Не пытайтесь меня крякнуть!</p></body></html>'
    return file('tasksheets/'+name+'/theory.html')

@the_app.route('/tasks/<name>')
def tasks(name):
    if pathsep in name or not isfile('tasksheets/'+name+'/tasks.html'):
        return file("forbidden.html", 403)
#       response.status = 403
#       return '<html><head><title>Задачи</title></head><body><h3>'\
#              'Замечание для умных</h3><p>Не пытайтесь меня крякнуть!</p></body></html>'
    return file('tasksheets/'+name+'/tasks.html')
