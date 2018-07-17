import os.path, subprocess, tempfile
from dkcareglaz.tester import run_solution, show_ok, superstrip

def prepare_contest(dir):
    return {task: (task, prepare_task(dir+'/'+task)) for task in os.listdir(dir) if os.path.isdir(dir+'/'+task)}

def prepare_task(dir):
    build_tester(dir)
    return base_tester.__get__(dir)

def base_tester(dir, elf, log):
    test_fmt_str = dir.replace('%', '%%')+"/tests/%02d"
    out_fmt_str = test_fmt_str + '.a'
    i = 1
    while os.path.exists(test_fmt_str % i):
        with open(test_fmt_str % i) as file: data = file.read()
        normal, stdout, stderr = run_solution(elf, data, log, 'Test #%d'%i, False)
        if not normal:
            i += 1
            continue
        with tempfile.NamedTemporaryFile(mode='w') as f:
            f.write(stdout)
            f.flush()
            if os.path.exists(dir+'/check'):
                ans = subprocess.call((dir+'/check', test_fmt_str % i, f.name, out_fmt_str % i))
            else:
                with open(out_fmt_str % i, encoding='utf-8', errors='replace') as file:
                    data = superstrip(file.read().replace('\r\n', '\n')).strip()
                stdout = superstrip(stdout.replace('\r\n', '\n')).strip()
                ans = data != stdout
        show_ok(log, ans)
        i += 1
    return True

def build_tester(dir):
    if not os.path.exists(dir+'/check'):
        with open("testlib.h") as src:
            with open(dir+'/testlib.h', 'w') as dst:
                dst.write(src.read())
        if subprocess.call(("g++", "--std=c++14", dir+'/check.cpp', "-o", dir+'/check')):
            print("Failed to build tester, will use cmp-test")
