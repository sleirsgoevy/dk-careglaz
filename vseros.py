import os.path, subprocess, tempfile, collections
from dkcareglaz.tester import run_solution, show_ok, superstrip, display_output

def prepare_contest(dir, debug=False, timeouts={}):
    return collections.OrderedDict((task, (task, prepare_task(dir+'/'+task, debug, timeouts.get(task, 1)))) for task in sorted(os.listdir(dir)) if os.path.isdir(dir+'/'+task))

def prepare_task(dir, debug=False, timeout=1):
    if os.path.exists(dir+'/files/check.cpp'):
        build_tester(dir, dir+'/files')
    else:
        build_tester(dir)
    return base_tester.__get__((dir, debug, timeout))

def base_tester(params, elf, log):
    dir, debug, timeout = params
    test_fmt_str = dir.replace('%', '%%')+"/tests/%02d"
    out_fmt_str = test_fmt_str + '.a'
    i = 1
    while os.path.exists(test_fmt_str % i):
        with open(test_fmt_str % i) as file: data = file.read()
        normal, stdout, stderr = run_solution(elf, data, log, 'Test #%d'%i, False, timeout=timeout)
        if not normal:
            i += 1
            if debug: display_output(data, stdout, stderr, log)
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
        if debug: display_output(data, stdout, stderr, log)
        i += 1
    return True

def build_tester(dir, dir2=None):
    if dir2 == None: dir2 = dir
    if not os.path.exists(dir+'/check'):
        with open("testlib.h") as src:
            with open(dir2+'/testlib.h', 'w') as dst:
                dst.write(src.read())
        if subprocess.call(("g++", "--std=c++14", dir2+'/check.cpp', "-o", dir+'/check')):
            print("Failed to build tester, will use cmp-test")
