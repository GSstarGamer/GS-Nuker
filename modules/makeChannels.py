import functions.PyUtls as utils
import asyncio
import random

name = 'Make channels'
description = 'Makes n number of channels with given name/names'

def execute():
    token = utils.binput('Token: ')
    id = utils.binput('Guild ID: ')
    channelName = utils.binput('Channel name (TIP: doing "channel1, channel2" will randomize channel name): ')
    amount = int(utils.binput('Amount of times: '))

    import discord
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        utils.bprint('Started')
        guild = client.get_guild(id)
        if guild is None:
            guild = await client.fetch_guild(id)
        if guild is not None:
            channel_names = channelName.split(', ')
            channel_creators = [guild.create_text_channel(random.choice(channel_names)) for _ in range(amount)]
            await asyncio.gather(*channel_creators)
            print(f"{amount} channels created.")
        else:
            print('Guild not found')
        utils.bprint('Done')
        await client.close()

    client.run(token)
