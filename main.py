import functions.PyUtls as utils
import os
import importlib
import json
import random
from time import sleep as wait
import sys
import requests
from dotenv import load_dotenv
import functions.discordRequests as discord
load_dotenv()

token = os.getenv('token')

utils.projectDetails.owner = 'GS_S.G'
utils.projectDetails.projectName = 'Discord server nuker 😎'
utils.projectDetails.version = '0.1'
utils.settings.logoColor = utils.colors.CVIOLET

with open('./assets/logo.txt', encoding='utf-8') as f:
    logo = f.read()

utils.settings.printCap = False
utils.settings.logo = logo
utils.settings.logoOnClear = True
utils.settings.centerLogo = True

utils.startUp(True)

modules = []

for index, file in enumerate(os.listdir('./modules')):
    if file.endswith(".py"):
        try:
            module = importlib.import_module(f"modules.{file[:-3]}")
            modules.append({'index': index, 'name': module.name,
                           'description': module.description, 'fileName': file})
        except Exception as e:
            utils.warn(str(e))
            exit()


def menu(proxy_to_use):
    print('-'*utils.columns)
    for module in modules:
        random_var = random.choice(utils.colors.list_of_colors)

        index = random_var+str(module["index"])+utils.colors.CEND
        name = utils.colors.CBEIGE+str(module["name"])+utils.colors.CEND
        desc = utils.colors.CGREEN+str(module["name"])+utils.colors.CEND
        print(f'{index} | Name: {name} | Description: {desc}')
    print('-'*utils.columns)

    ask = utils.binput('Please choose an option: ')
    try:
        if any(module["index"] == int(ask) for module in modules):
            for module in modules:
                if module["index"] == int(ask):
                    filename = module["fileName"]
                    file = importlib.import_module(f"modules.{filename[:-3]}")
                    file.execute(proxy_to_use, token)
        else:
            utils.bprint("Not a valid option")
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno

        utils.error(f'''
        exception: {e}
        exception_type: {exception_type}
        filename: {filename}
        line_number: {line_number}''')


def get_proxy(file):
    utils.bprint('Looking for proxy...')

    def checkProxie(proxie):
        proxie = {
            'http': 'http://'+proxie
        }
        headers = {
            'content-type': 'application/json',
            'Authorization': f'Bot {token}'
        }

        req = requests.get(
            f'https://discord.com/api/v10/users/@me', headers=headers, proxies=proxie)

        if req.status_code == 429:
            utils.bprint('Bad proxy looking new')
            return False
        else:
            return True

    req = requests.get(
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt')

    list_of_proxies = req.text.splitlines()

    while True:
        proxy = random.choice(list_of_proxies)
        if checkProxie(proxy):
            utils.success('Proxy got')
            return {'http': proxy}
            break
        else:
            pass


while True:
    proxy = get_proxy('http_proxies.txt')
    if discord.checkToken(token, proxy) == 404:
        utils.warn('Invalid token')
        exit()

    utils.clear()
    menu(proxy)
    utils.binput('Press enter to exit\n')
