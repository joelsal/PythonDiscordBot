import discord
from discord.ext import commands
from discord.utils import get
import os
import youtube_dl
import shutil

token = 'NjQ2NjUyNzQzMDI0NTA4OTc5.XdUiVA.uqK3XNWImg_J6VBXascNFfg1Uj8'
prefix = '!'
client = commands.Bot(command_prefix = prefix)

@client.event
async def on_ready():
    print('BOT IS ONLINE')

@client.command(pass_context=True, brief='Makes the bot join the same voice channel where the user is.')
async def join(ctx):    #Bot joins voice channel

    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"Bot has connected to {channel}\n")
        await ctx.send(f"Bot joined {channel}")

@client.command(pass_context=True, brief='Makes the bot leave the voice channel.')
async def leave(ctx):   #Bot leaves voice channel
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"Bot has left {channel}\n")
        await ctx.send(f"Bot left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel!")

@client.command(pass_context=True, brief='Plays the sound of any YouTube video.', description='Will automatically make the bot join on the same voice channel as the user if it has not joined already, then plays the sound of the YouTube-url on the same voice channel where the user is.')
async def play(ctx, url: str):   #Bot plays song

    try:
        channel = ctx.message.author.voice.channel
        voice = get(client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            print(f"Bot has connected to {channel}\n")
            await ctx.send(f"Bot joined {channel}")
    except:
        await ctx.send(f"No users in any of the voice channels!")
        return

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_queue = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued songs")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued song\n")
                print(f"Songs still in queue: {still_queue}")
                ctx.send(f"Number of songs still in queue: {still_queue}")
                song_is_there = os.path.isfile("song.mp3")
                if song_is_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.25

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("No songs were queued during the previous song\n")

    song_is_there = os.path.isfile("song.mp3")
    try:
        if song_is_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete old song file, but it's being played")
        await ctx.send("Music already playing")
        return
    
    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old queue folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old queue folder")


    await ctx.send("Fetching song...")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading song...\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed file: {file}\n")
            os.rename(file, "song.mp3")
    
    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.25

    newname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {newname[0]}")
    print("Playing")

@client.command(pass_context=True, brief='Pauses the current song.', description='Pauses the song at the moment the command was entered. The song can be resumed back from the same moment by typing !resume.')
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send(f"Music paused")
    else:
        print("Music failed to pause")
        await ctx.send("Music not playing, could not pause")

@client.command(pass_context=True, brief='Resumes the current song.', description='Used to resume a paused song. Type !pause to pause the currently playing song and then use !resume to resume it back to playing from where it was puased.')
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_paused():
        print("Music resumed")
        voice.resume()
        await ctx.send(f"Music resumed")
    else:
        print("Music could not be resumed")
        await ctx.send("Music not on pause, could not resume")

@client.command(pass_context=True, brief='Skips the current song.', description='Skips the currently playing song and automatically plays the next queued song if there are any. Also lets the user know how many songs there are queued at the moment.')
async def skip(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    queues.clear()

    try:
        if voice and voice.is_playing():
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_queue = length - 1
            print("Music stopped")
            voice.stop()
            await ctx.send(f"Music skipped, {still_queue} song(s) left in the queue!")
        else:
            print("Music failed to skip")
            await ctx.send("Music not playing, could not skip")
    except:
        voice.stop()
        await ctx.send(f"Music skipped, 0 song(s) left in the queue!")

queues = {}

@client.command(pass_context=True, brief='Queues songs to be played later.', description='Used to put songs onto a queue which will play automatically later, when the current song has ended.')
async def queue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    queue_size = len(os.listdir(DIR))
    queue_size += 1
    add_queue = True
    while add_queue:
        if queue_size in queues:
            queue_size += 1
        else:
            add_queue = False
            queues[queue_size] = queue_size

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{queue_size}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading song...\n")
        ydl.download([url])
    await ctx.send("Song added into a queue!")
    
    print("Song added to queue\n")

@client.command(pass_context=True, brief='Used to check the size of the of the song queue.')
async def size(ctx):
    try:
        DIR = os.path.abspath(os.path.realpath("Queue"))
        length = len(os.listdir(DIR))
        await ctx.send(f"{length} song(s) currently in queue!")
    except:
        await ctx.send("No song(s) currently in queue!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await client.process_commands(message)

client.run(token)