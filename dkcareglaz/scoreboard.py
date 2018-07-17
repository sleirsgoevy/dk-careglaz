import dkcareglaz.config as config, dkcareglaz.locale as locale
from os import listdir
from os.path import isfile, isdir, sep as pathsep
from bottle import route, response, request
from .login import authenticate
from collections import defaultdict
from .tester import import_tester
from html import escape
from .shower import file

def get_user_score(sheet, user):
    ok = 0
    fail = 0
    tasks = defaultdict(int)
    filename = 'scoreboard/{sheet}/{user}'.format(sheet=sheet, user=user)
    if isfile(filename):
        with open(filename) as file:
            for line in file:
                id, task = line.split()
                if isfile('submissions/{}.ok'.format(id)):
                    if tasks[task] <= 0:
                        tasks[task] = 1 - tasks[task]
                        ok += 1
                else:
                    if tasks[task] > 0:
                        ok -= 1
                        tasks[task] = -tasks[task]
                    tasks[task] -= 1
                    fail += 1
    return ((ok, -fail), user, tasks)

def format_user(user, tasks, all_tasks):
    ans = ''
    for task in sorted(all_tasks):
        ans += '<td'
        if tasks[task] > 0:
            ans += ' bgColor=lime>+'
            if tasks[task] > 1:
                ans += str(tasks[task]-1)
        elif tasks[task] < 0:
            ans += ' bgColor=red>' + str(tasks[task])
        else: ans += '>'
        ans += '</td>'
    ans += '</tr>'
    return ans

@route('/scoreboard/<sheet>')
def scoreboard(sheet):
    if pathsep in sheet or not isdir('scoreboard/'+sheet) or not config.allow_scoreboard:
        return file("forbidden.html", 403)
#       response.status = 403
#       return '<html><head><title>Таблица результатов</title></head><body><h3>'\
#              'Замечание для умных</h3><p>Не пытайтесь меня крякнуть!</p></body></html>'
    with open('tasksheets/{}/name.txt'.format(sheet)) as f:
        name = f.readline().strip()
    ans = '<html><head><title>{{scoreboard}} - {name}</title></head><body>'\
          '<h3>{{scoreboard}} - {name}</h3>'.format(name=escape(name))
    if authenticate(request.get_cookie('credentials', default='invalid')):
        ans += '<a href="../../submit/{sheet}">{{submit_sol}}</a>&nbsp;'\
               '<a href="../../submissions/{sheet}">{{yours}}</a>&nbsp;'\
               '<a href="../../logout">{{logout}}</a><br />'.format(sheet=sheet)
    ans += '<table cellspacing=0 border=1><tr><td></td>'
    user_scores = [get_user_score(sheet, user) for user in listdir('scoreboard/'+sheet)]
    user_scores.sort(key=lambda x: x[0])
    user_scores.reverse()
    tester = import_tester(sheet)
    for task in tester.tasks:
        ans += '<td>'+task+'</td>'
    ans += '</tr>'
    for i, (garbage, user, tasks) in enumerate(user_scores):
        with open('users/{}.real_name'.format(user)) as f:
            real_name = f.read()
        ans += '<tr><td>{no}. {name}</td>{fmt}'.format(name=escape(real_name), fmt=format_user(user, tasks, tester.tasks), no=i+1)
    ans += '</table></body></html>'
    return ans.format(**locale.get_locale())
