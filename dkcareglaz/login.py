import dkcareglaz.config as config, dkcareglaz.locale as locale
from .app import the_app
from bottle import request, response, redirect
from os.path import isfile
from os import unlink
from re import compile as re_compile
from hashlib import md5
from time import time
from .shower import file

correct = re_compile('^[a-zA-Z0-9_\-]+$')
number = re_compile('^[0-9]+(.[0-9]*)?$')

#LOGIN = """\
#<html>
#<head>
#<title>Вход в систему</title>
#</head>
#<body>
#<form method=post action="#">
#<label for=user>Имя пользователя:</label><br />
#<input id=user name=user /><br />
#<label for=pass>Пароль:</label><br />
#<input id=pass name=pass type=password /><br />
#<input type=submit value="Войти или зарегистрироваться" />
#</form>
#</body>
#</html>
#"""

#REGISTER = """\
#<html>
#<head>
#<title>Регистрация</title>
#</head>
#<body>
#<h3>Похоже, вы здесь впервые</h3>\
#<form method=post action="#">
#<input type=hidden name=user type=hidden value="{user}" />
#<input type=hidden name=pass type=hidden value="{pass_}" />
#<label for=real_name>Ваше реальное имя (не проверяется):</label><br />
#<input id=real_name name=real_name /><br />
#<label for=password>Повторите пароль:</label><br />
#<input id=password name=password type=password /><br />
#<input type=submit value="Зарегистрироваться" />
#</form>
#</body>
#</html>
#"""

LOGIN = open("login.html").read()
REGISTER = open("register.html").read()

@the_app.route('/login/<id>')
@the_app.route('/login-result/<id>')
def login(id):
    return LOGIN

def _authenticate():
    login = request.forms.get('user', default=None)
    pass_ = request.forms.get('pass', default=None)
    if login == None or pass_ == None:
        return file("forbidden.html", 403)
#       response.status = 403
#       return '<html><head><title>Вход в систему</title></head><body><h3>'\
#              'Замечание для умных</h3><p>Не пытайтесь меня крякнуть!</p></body></html>'
    if correct.match(login) == None:
        return file("invalid_nickname.html")
    hash = md5()
    hash.update(pass_.encode('utf-8'))
    hash = hash.digest().hex()
    if not isfile('users/{}.pass'.format(login)) and config.allow_register:
        real_name = request.forms.get('real_name', default=None)
        password = request.forms.get('password', default=None)
        if real_name == None or password == None:
            if (real_name == None) ^ (password == None):
                return file("forbidden.html", 403)
#               response.status = 403
#               return '<html><head><title>Вход в систему</title></head><body><h3>'\
#                      'Замечание для умных</h3><p>Не пытайтесь меня крякнуть!</p></body></html>'
            return REGISTER.format(user=login, pass_=pass_)
        real_name = bytes(map(ord, real_name)).decode('utf-8')
        if password != pass_:
            return file("diff_passwords.html", 403)
#               '<html><head><title>{registration}</title></head><body><h3>'\
#               '{diff_passwords}!</h3></body></html>'
        with open('users/{}.pass'.format(login), 'w') as f:
            f.write(hash)
        with open('users/{}.real_name'.format(login), 'w') as f:
            f.write(real_name)
    t = str(time())
    with open('sessions/'+t, 'w') as f:
        f.write(login+':'+hash)
    response.set_cookie('credentials', t, path="/")

@the_app.post('/login/<sheet>')
def do_login(sheet):
    return _authenticate() or redirect("../../submit/"+sheet)

@the_app.post('/login-result/<id>')
def do_login_result(id):
    return _authenticate() or redirect("../../result/"+sheet)

def authenticate(t):
    if number.match(t) == None:
        return None
    if not isfile('sessions/'+t):
        return None
    if int(time() - float(t)) not in range(86400):
        unlink('sessions/'+t)
        return None
    with open('sessions/'+t) as file:
        user, hash = file.read().split(':', 1)
    with open('users/{}.pass'.format(user)) as file:
        hash2 = file.read()
    if hash == hash2:
        return user
    return None

@the_app.route('/logout')
def logout():
    response.set_cookie('credentials', 'invalid')
    return redirect(config.redirect_on_logout)
