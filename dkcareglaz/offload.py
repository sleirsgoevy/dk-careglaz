import dkcareglaz.config as config, urllib.request, os, queue
from collections import OrderedDict

def compile_offload(id, log, *, ext='txt'):
    source = 'submissions/{}.src'.format(id)
    with open(source, 'rb') as file:
        return (file.read(), ext)

def test_offload(offload_setup, elf, log):
    task, urls = offload_setup
    src, ext = elf
    src = src.decode('latin-1')
    data = ['', 'Content-Disposition: form-data; name="task"\r\n\r\n'+task+'\r\n', 'Content-Disposition: form-data; name="solution"; filename="solution.%s"\r\n\r\n%s\r\n'%(ext, src), '--\r\n']
    while True:
        boundary = '-'*10+os.urandom(16).hex()
        for i in data:
            if boundary in i: break
        else: break
    data = ('--'+boundary).join(data).encode('latin-1')
    url, auth_token = urls.get()
    try: req = urlib.request.urlopen(urllib.request.Request(url+'/submit/test', data, {'Cookie': 'credentials='+auth_token}))
    except urllib.error.URLError as err: req = err
    if req.getcode() != 200 or not req.geturl().startswith(url+'/result/'):
        log.write('<font color=red>Unknown etwork error</font>\n')
        try:
            with os.popen('bash report.sh', 'w') as p:
                print(req.geturl(), file=p)
                print(repr(req.read()), file=p)
                print(repr(data), file=p)
        except: pass
        return False
    while True:
        try: req2 = urllib.request.urlopen(req.geturl()+'/api')
        except urllib.error.URLError as err: req2 = err
        data = req2.read().decode('utf-8')
        if data != 'not finished':
            break
    status, log_text = data.split('\n', 1)
    if status not in ('ok', 'not ok'):
        log.write('<font color=red>Unknown error</font>\n')
        try:
            with os.popen('bash report.sh', 'w') as p:
                print(repr(data), file=p)
        except: pass
        return False
    log.write(log_text)
    return status == 'ok'

def do_offload(tasks, urls):
    if config.auth_token != None: return tasks
    ans = OrderedDict()
    for id, (name, tester, *options) in tasks.items():
        if options:
            options = options[0]
        else:
            options = {}
        tester = test_offload.__get__((id, urls))
        options['compiler'] = compile_offload
        ans[id] = (name, tester, options)
    return ans
