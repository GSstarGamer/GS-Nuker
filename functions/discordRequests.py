import requests
import json
import queue
import functions.PyUtls as utils
from time import sleep as wait

my_queue = queue.Queue()

max_retrys = 5


def storeInQueue(f):
    def wrapper(*args):
        my_queue.put(f(*args))
    return wrapper


def checkToken(token, proxe):
    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bot {token}'
    }

    req = requests.get(
        f'https://discord.com/api/v10/users/@me', headers=headers, proxies=proxe)
    return req.status_code


@storeInQueue
def channelCreate(name, guildID, token, proxe):
    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bot {token}',
        'X-Audit-Log-Reason': 'GS at TOP'
    }

    body = {
        'type': 0,
        'name': name.replace(' ', '-'),
        'permission_overwrites': []
    }
    retrys = 0
    while True:
        if retrys >= 3:
            break
        req = requests.post(
            f'https://discord.com/api/v10/guilds/{guildID}/channels', json=body, headers=headers, proxies=proxe)
        data = json.loads(req.text)
        print(req.status_code)
        if req.status_code == 201:
            utils.success('Created channel')
            break
        elif req.status_code == 429:
            if not data['global']:
                utils.fail('Bot is dead try a diffrent bot')
            else:
                utils.fail(
                    f'Rate limited {data["retry_after"]} seconds, retrying')
                wait(.5)
        retrys += 1


def checkGuild(guildID, token, proxe):
    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bot {token}'
    }

    req = requests.get(
        f'https://discord.com/api/v10/guilds/{guildID}', headers=headers, proxies=proxe)

    return req.status_code


def guildDetails(guildID, token, proxe):
    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bot {token}'
    }

    req = requests.get(
        f'https://discord.com/api/v10/guilds/{guildID}', headers=headers, proxies=proxe)
    return req


def guildChannels(guildID, token, proxe):
    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bot {token}'
    }

    req = requests.get(
        f'https://discord.com/api/v10/guilds/{guildID}/channels', headers=headers, proxies=proxe)
    return json.loads(req.text)


@storeInQueue
def guildDetails(guildID, token, proxe):
    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bot {token}'
    }

    req = requests.get(
        f'https://discord.com/api/v10/guilds/{guildID}', headers=headers, proxies=proxe)

    return req


@storeInQueue
def deleteChannel(channelID, token, proxe):
    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bot {token}',
        'X-Audit-Log-Reason': 'GS at TOP'
    }

    retrys = 0
    while True:
        if retrys >= max_retrys:
            break
        req = requests.delete(
            f'https://discord.com/api/v10/channels/{channelID}', headers=headers, proxies=proxe)
        data = json.loads(req.text)
        if req.status_code == 200:
            utils.success(f'Deleted a channel')
            break
        elif req.status_code == 429:
            if not data['global']:
                utils.fail('Bot is dead try a diffrent bot')
            else:
                utils.fail(
                    f'Rate limited {data["retry_after"]} seconds, retrying')
                wait(data["retry_after"])
        retrys += 1
    return req
