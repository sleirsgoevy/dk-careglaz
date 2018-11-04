import dkcareglaz.config, dkcareglaz.locale
from bottle import route, app
from os import listdir
from html import escape
import dkcareglaz.login, dkcareglaz.shower, dkcareglaz.tester, dkcareglaz.scoreboard
from .app import the_app as application

@application.route('/')
def dkcareglaz():
    if not config.allow_main_page:
        return shower.file("forbidden.html", 403)
    ans = '<html><head><title>{testsys}</title></head><body>'\
          '<table sellspacing=0 border=1>'
    ansl = []
    for i in listdir('tasksheets'):
        with open('tasksheets/{}/name.txt'.format(i)) as file:
            with open('tasksheets/{}/sortid.txt'.format(i)) as file2: sortid = int(file2.read())
            name = file.readline().strip()
            ansl.append((sortid, ('<tr><td>{name}</td>'\
                    '<td><a href="theory/{i}">{{theory}}</a></td>'\
                    '<td><a href="tasks/{i}">{{tasks}}</a></td>'\
                    '<td><a href="submit/{i}">{{submit}}</a></td>'+
                    ('<td><a href="scoreboard/{i}">{{scoreboard}}</a></td>'
                    if config.allow_scoreboard else '')+'</tr>').format(name=escape(name), i=i)))
    ansl.sort()
    ansl.reverse()
    for i in ansl: ans += i[1]
    ans += '</table></body></html>'
#   print(ans)
    return ans.format(**locale.get_locale())
