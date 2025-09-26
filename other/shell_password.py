import http.client
from base64 import b64decode


def getShellPasswordBySn(sn):
    httpClient = http.client.HTTPConnection('10.192.9.1', 80, timeout=60)
    httpClient.request('GET', '/dataanalyze/hsmShellpwd?sn=%s&subSystemCallFlag=1' % sn)
    response = httpClient.getresponse()
    rc = '1'
    if (response.status == 200):
        content = response.read()
        import ast
        try:
            result_dict = ast.literal_eval(content.decode().split("\r\n")[0])
        except Exception as e:
            return (rc, str(e))

        if (result_dict['rc'] == '0'):
            rc = '0'
            result = decrypt(result_dict['message'])
        else:
            result = result_dict['message']

    else:
        result = 'request meet exception, http code: %s' % response.status

    return (rc, result)

def decrypt(shellpwd):
    newAndOld_ShellPwd = shellpwd.split(';')
    shellpwd_dict = {}
    shellpwd_dict['newpwd'] = newAndOld_ShellPwd[0].replace('shellpassword@','')
    return shellpwd_dict

def shell_password(sn):
    """ Get the shell password from service """
    _shell_password = ""
    for i in range(3):
        rc, result = getShellPasswordBySn(sn)
        if int(rc) == 0 and isinstance(result, dict):
            if 'newpwd' in result:
                _shell_password = b64decode(result['newpwd'])[::-1]
                break
    return str(_shell_password)[2:-3]


print(shell_password('123456'))