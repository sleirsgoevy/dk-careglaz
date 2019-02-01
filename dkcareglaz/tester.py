import os, dkcareglaz.config as config, dkcareglaz.locale as locale
from .app import the_app
from bottle import response, request
from .redirect import redirect
from os.path import isfile, isdir, sep as pathsep
from sys import modules
from imp import load_module, PY_SOURCE
from html import escape
from .login import authenticate
from subprocess import Popen, call, PIPE, TimeoutExpired
from threading import Thread, Lock
from .shower import file

def import_tester(name):
    modname = 'tester::'+name
    if modname in modules:
        return modules[modname]
    filename = 'tasksheets/{}/tester.py'.format(name)
    with open(filename) as file:
        ans = load_module(modname, file, filename, ('.py', 'r', PY_SOURCE))
    modules[modname] = ans
    return ans

@the_app.route('/submit/<sheet>')
def task_route(sheet):
    if pathsep in sheet or not isfile('tasksheets/{}/tester.py'.format(sheet)):
        return file("forbidden.html", 403)
    credentials = request.get_cookie('credentials', default='invalid')
    if credentials == 'invalid':
        return redirect("../../login/"+sheet)
    if not authenticate(credentials):
        return file("login_error.html", 401, True)
#       response.status = 403
#       return '<html><head><title>Не удалось авторизоваться</title></head><body>'\
#              '<h3>Не удалось авторизоваться</h3><p>Неверный пароль, попробуйте '\
#              '<a href="https://newsgoevy.pythonanywhere.com/dk-careglaz/login/{}">'\
#              'перезайти</a>.</p></body></html>'.format(sheet)
#       response.status = 403
#       return '<html><head><title>Сдать задачу</title></head><body><h3>'\
#              'Замечание для умных</h3><p>Не пытайтесь меня крякнуть!</p></body></html>'
    tester = import_tester(sheet)
    with open('tasksheets/{}/name.txt'.format(sheet)) as f: name = f.readline().strip()
    ans = '<html><head><title>{{submit_sol}} - {name}</title></head><body>'\
          '<a href="../submissions/{sheet}">{{submissions}}</a>&nbsp;'
    if config.allow_scoreboard:
        ans += '<a href="../scoreboard/{sheet}">{{scoreboard}}</a>&nbsp;'
    ans += '<a href="../logout">{{logout}}</a><br />'
    if hasattr(tester, 'intro'):
        ans += tester.intro
    ans += '<form action="#" method=post enctype="multipart/form-data">'\
           '<select name=task><option disabled selected style="display: none">'\
           '{{select_task}}</option>'
    ans = ans.format(sheet=sheet, name=name)
    for id, (name, do_test, *args) in tester.tasks.items():
        if args and args[0].get('hidden', False): continue
        ans += '<option value={id}>{name}</option>'.format(name=escape(name), id=id)
    ans += '</select><input type=file name=solution /><input type=submit value="Отправить!" />'\
           '</form></body></html>'
    response.set_cookie('credentials', credentials, max_age=86400, path="/")
    return ans.format(**locale.get_locale())

@the_app.post('/submit/<sheet>')
def task_sumbit(sheet):
    credentials = request.get_cookie('credentials', default='invalid')
    if credentials == 'invalid':
        return redirect("../../login/"+sheet)
    user = authenticate(credentials)
    if not user:
        return file("login_error.html", 401, True)
    if pathsep in sheet or not isfile('tasksheets/{}/tester.py'.format(sheet)):
        return redirect("forbidden.html", 403)
#       response.status = 403
#       return '<html><head><title>Сдать задачу</title></head><body><h3>'\
#              'Замечание для умных</h3><p>Не пытайтесь меня крякнуть!</p></body></html>'
    tester = import_tester(sheet)
    task = request.forms.get('task')
    if task not in tester.tasks:
        return file("forbidden.html", 403)
    solution = request.files.get('solution')
    if solution == None:
        return file("no_file.html", 200)
    solution_id = get_solution_id(user)
    with open('scoreboard/{sheet}/{user}'.format(sheet=sheet, user=user), 'a') as f:
        f.write(solution_id+' '+task+'\n')
    save_solution(solution, solution_id)
    if hasattr(tester_thread, 'executor'):
        tester_thread.executor.submit(tester_thread, tester, tester.tasks[task], solution_id, solution.raw_filename.split('.')[-1])
    else:
        Thread(target=tester_thread, args=(tester, tester.tasks[task], solution_id, solution.raw_filename.split('.')[-1])).start()
    return redirect("../../result/"+solution_id)

def tester_thread(tester0, task_desc, solution_id, ext='cpp'):
    tester = task_desc[1]
    compiler = task_desc[2]['compiler'] if len(task_desc) > 2 else getattr(tester, 'compile_solution', compile_solution)
    with open('submissions/{}.log'.format(solution_id), 'w') as log:
        try:
            elf, cmd = compiler(solution_id, log, ext=ext)
            if (elf != None or cmd != None) and tester(cmd, log):
                with open('submissions/{}.ok'.format(solution_id), 'w'): pass
            if elf != None: os.unlink(elf)
        except:
            import traceback, sys
            log.write('<font color=red>{}</font>'.format(escape(''.join(traceback.format_exception(*sys.exc_info())))))
        finally:
            with open('submissions/{}.finished'.format(solution_id), 'w'): pass

if config.testing_thread_limit != None:
    import concurrent.futures
    tester_thread.executor = concurrent.futures.ThreadPoolExecutor(config.testing_thread_limit)

@the_app.route('/result/<id>')
def do_show_result(id):
    credentials = request.get_cookie('credentials', default='invalid')
    if credentials == 'invalid':
        response.status = 302
        response['Location'] = '../login-result/'+id
        return ''
    user = authenticate(credentials)
    if not user:
        return file("login_error.html", 401, True)
#       response.status = 403
#       return '<html><head><title>Не удалось авторизоваться</title></head><body>'\
#              '<h3>Не удалось авторизоваться</h3><p>Неверный пароль, попробуйте '\
#              '<a href="https://newsgoevy.pythonanywhere.com/dk-careglaz/login">перезайти</a>.</p></body></html>'
    if pathsep in id or not isfile('submissions/{}.user'.format(id)):
        return file("forbidden.html", 403)
#       response.status = 403
#       return '<html><head><title>Протокол</title></head><body><h3>'\
#              'Замечание для умных</h3><p>Не пытайтесь меня крякнуть!</p></body></html>'
    with open('submissions/{}.user'.format(id)) as f:
        if f.read() != user:
            return file("not_yours.html", 403)
#           response.status = 403
#           return '<html><head><title>Протокол</title><head><body><h3>'\
#                  'Это не ваше решение</h3><p>Вы можете смотреть протокол только своих решений</p></body></html>'
    return show_result(id)

def show_result(id):
    if not isfile('submissions/{}.finished'.format(id)):
        return '<html><head><title>{{protocol}}{id}</title></head><body>'\
               '<a href="/dk-careglaz/logout">{{logout}}</a><br />'\
               '<p>{{not_finished}}</p>'\
               '<script>setTimeout(function(){{{{'\
               'document.location.href=document.location.href'\
               ';}}}}, 1000)</script>'\
               '</body></html>'.format(id=id).format(**locale.get_locale())
    ans = '<html><head><title>{{protocol}}{}</title></head><body>'\
          '<a href="../logout">{{logout}}</a><br /><pre>\n'.format(id)
    with open('submissions/{}.log'.format(id)) as file:
        ans += file.read().replace('{', '{{').replace('}', '}}')
    ans += '\n</pre></body></html>'
    return ans.format(**locale.get_locale())

def get_solution_id(user):
    with get_solution_id.lock:
        with open('submissions/id.txt') as file: id = str(int(file.readline())+1)
        with open('submissions/id.txt', 'w') as file: file.write(id)
    with open('submissions/{}.user'.format(id), 'w') as file: file.write(user)
    return id

get_solution_id.lock = Lock()

def save_solution(upload, id):
    upload.save('submissions/{}.src'.format(id))

def compile_solution(id, log, *, cmd="bash compile.sh %(src)s %(dst)s %(ext)s", ext='cpp', timeout=10):
    source = 'submissions/{}.src'.format(id)
    elf = 'submissions/{}.elf'.format(id)
    try:
        p = Popen(cmd % {'src': source, 'dst': elf, 'ext': ext}, shell=True, stdout=PIPE, stderr=PIPE)
        if p.wait(timeout):
            log.write(escape(p.stderr.read().decode('utf-8', 'replace')))
            log.write('<font color=red>Compilation failed!</font>')
            return (None, None)
    except TimeoutExpired:
        log.write(escape(p.stderr.read().decode('utf-8', 'replace')))
        log.write('<font color=red>Compilation timed out!</font>')
        return (None, None)
    log.write(escape(p.stderr.read().decode('utf-8', 'replace')))
    log.write('<font color=green>Compilation succeeded!</font>\n')
    return (elf, p.stdout.read().decode('utf-8'))

def run_solution(elf, input, log, name, do_superstrip = True, timeout=1, encoding='utf-8'):
    log.write(escape(name)+' ... ')
    input = input.encode(encoding)
    popen = Popen(elf, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    try:
        popen.stdin.write(input)
        popen.stdin.close()
    except OSError: pass
    normal = True
    try: exitcode = popen.wait(timeout=timeout)
    except TimeoutExpired:
        popen.kill()
        log.write('<font color=red>TIMED OUT</font>\n')
        normal = False
    if normal and exitcode:
        log.write('<font color=red>RUNTIME ERROR</font>'\
                  ' (exit code {})\n'.format(exitcode))
        normal = False
    out = popen.stdout.read().decode(encoding, 'replace')
    if do_superstrip:
        out = superstrip(out)
    return (normal,
            out,
            popen.stderr.read().decode('utf-8', 'replace'))

def display_output(stdin, stdout, stderr, log):
    log.write('input test\n')
    log.write(escape(stdin)+'\n')
    log.write('program output\n')
    log.write(escape(stdout)+'\n')
    if stderr != '':
        log.write('<font color=red>error output\n')
        log.write(escape(stderr)+'</font>\n')

def show_ok(log, wa):
    if not wa: log.write('<font color=green>OK</font>\n')
    else: log.write('<font color=red>WRONG ANSWER</font>\n')
    return wa

@the_app.route('/submissions/<sheet>')
def view_submissions(sheet):
    credentials = request.get_cookie('credentials', default='invalid')
    if credentials == 'invalid':
        return redirect("../../login-result/"+sheet)
#       response.status = 302
#       response['Location'] = 'https://newsgoevy.pythonanywhere.com/dk-careglaz/login-result/'+id
#       return ''
    user = authenticate(credentials)
    if not user:
        return file("login_error.html", 401, True)
#       response.status = 403
#       return '<html><head><title>Не удалось авторизоваться</title></head><body>'\
#              '<h3>Не удалось авторизоваться</h3><p>Неверный пароль, попробуйте '\
#              '<a href="https://newsgoevy.pythonanywhere.com/dk-careglaz/login">перезайти</a>.</p></body></html>'
    if pathsep in sheet or not isdir('scoreboard/{sheet}'.format(sheet=sheet)) or not isfile('users/{user}.real_name'.format(user=user)):
        return file("forbidden.html", 403)
#       response.status = 403
#       return '<html><head><title>Протокол</title></head><body><h3>'\
#              'Замечание для умных</h3><p>Не пытайтесь меня крякнуть!</p></body></html>'
    ans = '<html><head><title>{{yours}}</title></head><body>'\
          '<a href="../submit/{sheet}">{{submit_sol}}</a>&nbsp;'
    if config.allow_scoreboard:
        ans += '<a href="../scoreboard/{sheet}">{{scoreboard}}</a>&nbsp;'
    ans += '<a href="../logout">{{logout}}</a><br />'
    ans = ans.format(sheet=sheet)
    if isfile('scoreboard/{sheet}/{user}'.format(sheet=sheet, user=user)):
        with open('scoreboard/{sheet}/{user}'.format(sheet=sheet, user=user)) as f:
            for line in f:
                i, task = line.split()
                ans += '<a href="../result/{i}">{{solution}}{i} ({{task}} {task})</a><br />'.format(i=i, task=task)
    ans += '</body></html>'
    return ans.format(**locale.get_locale())

def superstrip(s):
    return '\n'.join(map(str.rstrip, s.split('\n')))

def compile_output_only(id, log, *, ext=None):
    source = 'submissions/{}.src'.format(id)
    import shlex
    return (None, 'cat '+shlex.quote(source))
