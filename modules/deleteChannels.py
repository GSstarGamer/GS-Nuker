import functions.PyUtls as utils
import asyncio


name = 'Delete all channels'
description = 'Deletes all channels in server'


def execute():
    token = utils.binput('Token: ')
    id = int(utils.binput('Guild ID: '))

    import discord
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        await client.fetch_guild(id)
        guild = client.get_guild(id)

        if guild is not None:
            utils.bprint(f'Started with {len(guild.text_channels)} channels')

            async def delete_channel(channel):
                await channel.delete()
                utils.success(f"{channel.name} has been deleted.")
            await asyncio.gather(*[delete_channel(channel) for channel in guild.text_channels])
        else:
            print('Guild not found')
        utils.bprint('Done')
        await client.close()


    client.run(token)
