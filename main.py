import functions.PyUtls as utils
import os
import importlib
import json
import random
from time import sleep as wait


logo = ''

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
            modules.append({'index': index, 'name': module.name, 'description': module.description, 'fileName': file})
        except:
            pass
 
def menu():
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
                    file.execute()
        else:
            utils.bprint("Not a valid option")
    except Exception as e:
        utils.error(e)

while True:
    utils.clear()
    menu()
    utils.binput('Press enter to exit\n')