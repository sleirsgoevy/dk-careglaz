from collections import OrderedDict
from dkcareglaz.tester import show_ok, run_solution, display_output
import random

def test_A(elf, log):
    out = True
    normal, stdout, stderr = run_solution(elf, '', log, 'Test #1', False)
    if normal:
        if show_ok(log, stdout != 'Hello, world!\n'): out = False
    else: out = False
    display_output('', stdout, stderr, log)
    return out

def gen_B():
    yield 179
    for i in range(20):
        yield random.randrange(1, (1<<31)-1)

def test_B(elf, log):
    out = True
    for i, n in enumerate(gen_B()):
        normal, stdout, stderr = run_solution(elf, str(n)+'\n', log, 'Test #{}'.format(i+1), False)
        if normal:
            if show_ok(log, stdout != 'The next number for the number {cur} is {next}.\n'\
                                      'The previous number for the number {cur} is {prev}.\n'
                                      .format(cur=n, next=n+1, prev=n-1)): out = False
        else: out = False
        display_output(str(n)+'\n', stdout, stderr, log)
        if not out: break
    return out

def gen_C():
    yield (3, 14)
    for i in range(20):
        a = random.randrange(1, (1<<31)-1)
        b = random.randrange(max(1, a-5), (1<<31)-1)
        yield(a, b)

def test_C(elf, log):
    out = True
    for i, (a, b) in enumerate(gen_C()):
        stdin = '{}\n{}\n'.format(a, b)
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            if show_ok(log, stdout != '{} {}\n'
                                      .format(*divmod(b, a))): out = False
        else: out = False
        display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

def test_D(elf, log):
    out = True
    for i, n in enumerate(gen_B()):
        stdin = str(n)+'\n'
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            if show_ok(log, stdout != stdin[-2:]): out = False
        else: out = False
        display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

def test_E(elf, log):
    out = True
    for i, n in enumerate(gen_B()):
        stdin = str(n)+'\n'
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            if show_ok(log, stdout != stdin[-3]+'\n'): out = False
        else: out = False
        display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

def gen_F():
    yield 179
    for i in range(20):
        yield random.randrange(100, 1000)

def test_F(elf, log):
    out = True
    for i, n in enumerate(gen_F()):
        stdin = str(n)+'\n'
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            if show_ok(log, stdout != str(sum(map(int, stdin[:-1])))+'\n'): out = False
        else: out = False
        display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

def gen_G():
    yield (7, 8)
    yield (8, 10)
    for i in range(20):
        b = random.randrange(1, (1<<30))<<1
        if random.random() >= 0.5:
            a = b - 2
        else:
            a = b - 1
        yield (a, b)

def test_G(elf, log):
    out = True
    for i, (a, b) in enumerate(gen_G()):
        stdin = str(a)+'\n'
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            if show_ok(log, stdout != str(b)+'\n'): out = False
        else: out = False
        display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

def gen_H():
    yield (2, 1, 3, 4)
    for i in range(20):
        yield (random.randrange(1, 1<<14) for i in range(4))

def test_H(elf, log):
    out = True
    for i, (a, b, c, d) in enumerate(gen_H()):
        stdin = '{}\n{}\n{}\n{}\n'.format(a, b, c, d)
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            if show_ok(log, stdout != str(2*(d*(a+b)-b+c)-a)+'\n'): out = False
        else: out = False
        display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

def gen_I():
    yield (20, 21, 22)
    for i in range(20):
        yield tuple(random.randrange(1, 1<<29) for i in range(3))

def test_I(elf, log):
    out = True
    for i, (a, b, c) in enumerate(gen_I()):
        stdin = '{}\n{}\n{}\n'.format(a, b, c)
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            if show_ok(log, stdout != str(sum(map(sum, map(2 .__rdivmod__, (a, b, c)))))+'\n'): out = False
        else: out = False
        display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

def gen_J():
    yield 150
    yield 1441
    for i in range(20):
        yield random.randrange(1, 1<<31)

def test_J(elf, log):
    out = True
    for i, n in enumerate(gen_J()):
        stdin = str(n)+'\n'
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            if show_ok(log, stdout != '{} {}\n'.format((n // 60) % 24, n % 60)): out = False
        else: out = False
        display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

def gen_K():
    yield 3602
    yield 129700
    for i in range(20):
        yield random.randrange(1, 1<<31)

def test_K(elf, log):
    out = True
    for i, n in enumerate(gen_K()):
        stdin = str(n)+'\n'
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            if show_ok(log, stdout != '%d:%02d:%02d\n'%((n // 3600) % 24, (n // 60) % 60, n % 60)): out = False
        else: out = False
        display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

def gen_L():
    yield (3, 7)
    for i in range(20):
        yield (random.randrange(1, 1<<31), random.randrange(1, 1<<31))

def test_L(elf, log):
    out = True
    for i, (a, b) in enumerate(gen_L()):
        stdin = '{}\n{}\n'.format(a, b)
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            if show_ok(log, stdout != '{} {}\n'.format(b, a)): out = False
        else: out = False
        display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

def test_N(elf, log):
    out = True
    for i, n in enumerate((3, 2, 1, 4, 5, 6, 7, 8, 9, 10)):
        stdin = str(n)+'\n'
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            x = 110 * (n // 2) + 60 * (n % 2) - 15
            if show_ok(log, stdout != '{} {}\n'.format(9+x//60, x%60)): out = False
        else: out = False
        display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

def gen_O():
    yield (10, 15, 2, 1015)
    yield (2, 50, 4, 250)
    for i in range(20):
        k, n = (random.randrange(1, 1<<14) for i in range(2))
        yield (k//100, k%100, n, k)

def test_O(elf, log):
    out = True
    for i, (a, b, c, d) in enumerate(gen_O()):
        stdin = '{}\n{}\n{}\n'.format(a, b, c)
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            k = d * c
            if show_ok(log, stdout != '{} {}\n'.format(k // 100, k % 100)): out = False
        else: out = False
        display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

def gen_P():
    yield (1, 1, 1, 2, 2, 2, 3661)
    yield (1, 2, 30, 1, 3, 20, 50)
    for i in range(20):
        a = random.randrange(86400)
        n = random.randrange(1, 86400)
        b = a + n
        yield (a // 3600, (a // 60) % 60, a % 60,
               (b // 3600) % 24, (b // 60) % 60, b % 60, n)

def test_P(elf, log):
    out = True
    for i, (a, b, c, d, e, f, x) in enumerate(gen_P()):
        stdin = '{}\n{}\n{}\n{}\n{}\n{}\n'.format(a, b, c, d, e, f)
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            if show_ok(log, stdout != str(x)+'\n'): out = False
        else: out = False
        display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

def gen_Q():
    yield (700, 750)
    yield (700, 2100)
    for i in range(20):
        a = random.randrange(1, (1<<29)-1)
        b = random.randrange(max(1, a-5), (1<<29)-1)
        yield(a, b)

def test_Q(elf, log):
    out = True
    for i, (a, b) in enumerate(gen_Q()):
        stdin = '{}\n{}\n'.format(a, b)
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            if show_ok(log, stdout != str((b + a - 1) // a)+'\n'): out = False
        else: out = False
        display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

def gen_R():
    yield (7, 30)
    yield (7, 28)
    for i in range(20):
        a = random.randrange(1, (1<<31)-1)
        b = random.randrange(max(1, a-5), (1<<31)-1)
        yield(a, b)

def test_R(elf, log):
    out = True
    for i, (a, b) in enumerate(gen_C()):
        stdin = '{}\n{}\n'.format(a, b)
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            if show_ok(log, stdout != str((-b) % a)+'\n'): out = False
        else: out = False
        display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

def gen_S():
    yield (10, 3, 2)
    for i in range(20):
        b = random.randrange(2, 1<<29)
        a = random.randrange(max(1, b-5), 1<<29)
        c = random.randrange(1, b)
        yield (a, b, c)

def test_S(elf, log):
    out = True
    for i, (a, b, c) in enumerate(gen_S()):
        stdin = '{}\n{}\n{}\n'.format(a, b, c)
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            if show_ok(log, stdout != str((a+b-2*c-1)//(b-c))+'\n'): out = False
        else: out = False
        display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

def gen_T():
    yield (60, 2)
    yield (-1, 1)
    for i in range(20):
        a = random.randint(1, 108)
        b = random.randrange(1, 109)
        if random.random() >= 0.5: a = -a
        yield(a, b)

def test_T(elf, log):
    out = True
    for i, (a, b) in enumerate(gen_T()):
        stdin = '{}\n{}\n'.format(a, b)
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            if show_ok(log, stdout != str(a * b % 109)+'\n'): out = False
        else: out = False
        display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

def gen_U():
    yield ('2002', '2002')
    digits = '0123456789'
    for i in range(20):
        a = random.choice(digits)
        b = random.choice(digits)
        if random.random() * 9 < 4:
            c = b
        else:
            c = random.choice(digits)
        if random.random() * 9 < 4:
            d = a
        else:
            d = random.choice(digits)
        n = a + b + c + d
        while len(n) > 1 and n[0] == '0': n = n[1:]
        yield (a + b + c + d, n)

def test_U(elf, log):
    out = True
    for i, (n, m) in enumerate(gen_U()):
        stdin = '{}\n'.format(m)
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            if show_ok(log, (stdout.strip() != '1') == (n[0] == n[3] and n[1] == n[2])): out = False
        else: out = False
        display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

def gen_V():
    yield (2, 8)
    yield (8, 2)
    yield (3, 5)
    for i in range(20):
        if random.random() < 0.5:
            a = random.randint(1, 1<<14)
            k = random.randint(1, 1<<14)
            b = a * k
            if random.random() < 0.5:
                yield (a, b)
            else:
                yield (b, a)
        else:
            yield (random.randint(1, 1<<28), random.randint(1, 1<<28))

def test_V(elf, log):
    out = True
    for i, (a, b) in enumerate(gen_V()):
        stdin = '{}\n{}\n'.format(a, b)
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            if show_ok(log, (stdout.strip() == '1') != ((a % b)*(b % a) == 0)): out = False
        else: out = False
        display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

def gen_W():
    yield (12, 34, 10, 34, 12, 35, 10, 36)
    yield (12, 34, 10, 0, 2, 34, 14, 0)
    for i in range(20):
        a = random.randrange(1440)
        b = random.randrange(1440)
        n = random.randrange(1, 1440)
        a2 = a + n
        b2 = b + 2 * n
        yield (a // 60, a % 60, b // 60, b % 60, (a2 // 60) % 24, a2 % 60, (b2 // 60) % 24, b2 % 60)

def test_W(elf, log):
    out = True
    for i, (a, b, c, d, e, f, g, h) in enumerate(gen_W()):
        stdin = '{}\n{}\n{}\n{}\n{}\n{}\n'.format(a, b, c, d, e, f)
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            if show_ok(log, stdout != '{} {}\n'.format(g, h)): out = False
        else: out = False
        if i < 2: display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

def gen_X():
    yield 2
    for i in range(20):
        yield random.randrange(1, (1<<31)-1)

def test_X(elf, log):
    out = True
    for i, n in enumerate(gen_X()):
        stdin = str(n)+'\n'
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            if show_ok(log, stdout != str(n + n % 2 - 1)+'\n'): out = False
        else: out = False
        if not i: display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

def gen_Y():
    yield (8, 5)
    yield (5, 8)
    yield (5, 5)
    for i in range(20):
        yield tuple(random.randrange(1, 1<<28) for i in range(2))

def test_Y(elf, log):
    out = True
    for i, (a, b) in enumerate(gen_Y()):
        stdin = '{}\n{}\n'.format(a, b)
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            if show_ok(log, stdout != str(max(a, b))+'\n'): out = False
        else: out = False
        display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

def gen_Z():
    yield (10, 5, 2, 1)
    yield (13, 5, 3, 2)
    yield (14, 5, 3, 2)
    yield (13, 9, 4, 1)
    yield (1, 5, 3, 2)
    for i in range(20):
        b = random.randrange(2, 1<<35)
        a = random.randrange(max(1, b-5), 1<<35)
        c = random.randrange(1, b)
        d = b % c
        yield (a, b, c, d)

def test_Z(elf, log):
    out = True
    for i, (a, b, c, d) in enumerate(gen_Z()):
        stdin = '{}\n{}\n{}\n'.format(a, b, c)
        normal, stdout, stderr = run_solution(elf, stdin, log, 'Test #{}'.format(i+1))
        if normal:
            if show_ok(log, stdout != str(((a-d)//(b-d)*(b//c) if a >= b else 0))+'\n'): out = False
        else: out = False
        if i < 5: display_output(stdin, stdout, stderr, log)
        if not out: break
    return out

tasks = OrderedDict()
tasks['A'] = ('Задача A. Hello, world!', test_A)
tasks['B'] = ('Задача B. Следующее и предыдущее', test_B)
tasks['C'] = ('Задача C. Дележ яблок', test_C)
tasks['D'] = ('Задача D. Последняя цифра', test_D)
tasks['E'] = ('Задача E. Число десятков', test_E)
tasks['F'] = ('Задача F. Сумма цифр', test_F)
tasks['G'] = ('Задача G. Следующее четное', test_G)
tasks['H'] = ('Задача H. Шнурки', test_H)
tasks['I'] = ('Задача I. Парты', test_I)
tasks['J'] = ('Задача J. Электронные часы - 1', test_J)
tasks['K'] = ('Задача K. Электронные часы - 2', test_K)
tasks['L'] = ('Задача L. Обмен значений - 1', test_L)
tasks['M'] = ('Задача M. Обмен значений - 2', test_L)
tasks['N'] = ('Задача N. Конец уроков', test_N)
tasks['O'] = ('Задача O. Стоимость покупки', test_O)
tasks['P'] = ('Задача P. Разность времен', test_P)
tasks['Q'] = ('Задача Q. Автопробег', test_Q)
tasks['R'] = ('Задача R. Дележ яблок - 2', test_R)
tasks['S'] = ('Задача S. Улитка', test_S)
tasks['T'] = ('Задача T. МКАД', test_T)
tasks['U'] = ('Задача U. Симметричное число', test_U)
tasks['V'] = ('Задача V. Проверьте делимость', test_V)
tasks['W'] = ('Задача W. Часы', test_W)
tasks['X'] = ('Задача X. Турнир', test_X)
tasks['Y'] = ('Задача Y. Максимум', test_Y)
tasks['Z'] = ('Задача Z. Детали', test_Z)
