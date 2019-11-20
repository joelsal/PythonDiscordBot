import discord
from discord.ext import commands

token = 'NjQ2NjUyNzQzMDI0NTA4OTc5.XdUiVA.uqK3XNWImg_J6VBXascNFfg1Uj8'

client = commands.Bot(command_prefix = '!')


joppe = '31ed5972-5576-46da-b91d-9c8499c2f732'
marko = 'ada4b1f0-b3a3-4f56-bbf5-56e36a357e5b'

stats = 'https://r6stats.com/stats/'


@client.event
async def on_ready():
    print('ready')

@client.event
async def on_member_join(member):
    print(f'{member} has joined the server!')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!hei':
        response = 'Moi!'
        await message.channel.send(response)

    if message.content == 'netsky':
        await message.channel.send('https://www.youtube.com/watch?v=X56hc3e3mn0')

    if message.content == '!stats marko':
        await message.channel.send(stats + marko)
    if message.content == '!stats joppe':
        await message.channel.send(stats + joppe)

    if message.content == "!stats":
        await message.channel.send('Type !stats <person>')



client.run(token)