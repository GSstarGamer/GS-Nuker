import requests


def checkProxie(proxie):
    proxie = {
        'http': 'http://'+proxie
    }
    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bot MTA2MzExNjUxOTYwMjY2MzU1NA.GyWJ2f.QStgJo4UaYrST_8LUXqanEleAy7tMjyfik7aa8'
    }

    req = requests.get(
        f'https://discord.com/api/v10/users/@me', headers=headers, proxies=proxie)

    if req.status_code == 429:
        return False
    else:
        return True


def proxies():
    with open('http_proxies.txt', 'r') as f:
        text = f.read()

    proxies_dic = {}
    for line in text.splitlines():
        if line == '':
            pass

        if checkProxie(line):
            return {'http': 'http://'+line}
            break
        else:
            print('bad')
            pass

    return False
