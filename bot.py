import discord
import random
from discord.ext import commands
from discord.voice_client import VoiceClient

token = 'NjQ2NzU0MDEzNjE4MTEwNDg3.XdVu2Q.nLPKTHsiQ8kC2mvxdRZfSKxEf-c'

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

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    possible_responses = [
        'Totta helvetissä', #JOO
        'Empä tiiä',        #EHKÄ
        'No ei vitussa',    #EI
    ]

    if message.content == '!random':
        await message.channel.send(random.choice(possible_responses))

    if message.content == '!hei':
        response = 'Moi ' + str(message.author)[:-5] + '!'
        await message.channel.send(response)

    if message.content == 'netsky':
        await message.channel.send('https://www.youtube.com/watch?v=X56hc3e3mn0')

    if message.content == '!stats marko':
        await message.channel.send(stats + marko)

    if message.content == '!stats joppe':
        await message.channel.send(stats + joppe)

    if message.content == "!stats":
        await message.channel.send('Type !stats <person>')

    if message.content == "!vanukas":
        await message.channel.send('päivän tekee paremmaks')

    if message.content == "!msg amount":
        await message.channel.send()

    if message.content == "!grandiosa":
        await message.channel.send('https://www.youtube.com/watch?v=wW7rTjxqxV4')

    if message.content == "musta mies":
        await message.channel.send('MUTTA TÄÄHÄN ON MUSTA MIES', tts=True)

    if message.content == "janne":
        await message.channel.send('vittu mikä homo', tts=True)


client.run(token)