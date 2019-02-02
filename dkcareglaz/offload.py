import dkcareglaz.config as config, urllib.request, os, queue
from collections import OrderedDict

def compile_offload(id, log, *, ext='txt'):
    source = 'submissions/{}.src'.format(id)
    with open(source, 'rb') as file:
        return (None, (file.read(), ext))

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
    data = ('--'+boundary+'\r\n').join(data).encode('latin-1')
    url, sheet, auth_token = urls.get()
    try:
        req = urllib.request.urlopen(urllib.request.Request(url+'/submit/'+sheet, data, {'Cookie': 'credentials='+auth_token, 'Content-Type': 'multipart/form-data; boundary='+boundary}))
        assert req.getcode() == 200 and req.geturl().startswith(url+'/result/'), req.read()
        while True:
            req2 = urllib.request.urlopen(urllib.request.Request(req.geturl()+'/api', None, {'Cookie': 'credentials='+auth_token}, method='GET'))
            data = req2.read().decode('utf-8')
            if data != 'not finished':
                break
        status, log_text = data.split('\n', 1)
        assert status in ('ok', 'not ok'), repr(data)
        log.write(log_text)
        return status == 'ok'
    finally:
        urls.put((url, sheet, auth_token))

def do_offload(tasks, urls):
    q = queue.Queue()
    for i in urls: q.put(i)
    if config.auth_token != None: return tasks
    ans = OrderedDict()
    for id, (name, tester, *options) in tasks.items():
        if options:
            options = options[0]
        else:
            options = {}
        tester = test_offload.__get__((id, q))
        options['compiler'] = compile_offload
        ans[id] = (name, tester, options)
    return ans
