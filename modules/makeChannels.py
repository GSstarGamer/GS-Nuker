import functions.PyUtls as utils
import random
import requests
import json
import functions.discordRequests as discord
import threading as thr
import queue

name = 'Make channels'
description = 'Makes n number of channels with given name/names'

threads = []

my_queue = queue.Queue()


def execute(proxe, token):
    id = utils.binput('Guild ID: ')
    channelName = utils.binput(
        'Channel name (TIP: doing "channel1, channel2" will randomize channel name): ').split(', ')
    amount = int(utils.binput('Amount of times: '))

    # id = '970203723819282432'

    if discord.checkGuild(id, token, proxe) == 404:
        utils.warn('Bot is not in guild')
        return

    if len(discord.guildChannels(id, token, proxe)) >= 500:
        utils.warn('Server is at maximum cap')
        return

    list_of_channels = discord.guildChannels(id, token, proxe)

    times_created = 0
    for i in range(amount):
        thread = thr.Thread(target=discord.channelCreate, args=(
            random.choice(channelName), id, token, proxe))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
        times_created += 1
    utils.bprint(
        f"{len(discord.guildChannels(id, token, proxe))-len(list_of_channels)} channels created.")
