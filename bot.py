#IMPORTS
import discord
from discord.ext import commands
from discord.utils import get
import os
import youtube_dl
import shutil

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

token = ''   #DISCORD BOT TOKEN

prefix = '!'                                    #!-prefix for all commands
client = commands.Bot(command_prefix = prefix)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@client.event
async def on_ready():           
    print('BOT IS ONLINE')  #Called when bot is ready to use!

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@client.command(pass_context=True, brief='Makes the bot join the same voice channel where the user is.', description='Makes the bot join the same voice channel where the user is. If the bot is on another voice channel, upon entering this command, the bot will move into the same channel as the user.')
async def join(ctx):    #JOIN COMMAND --- !join
    try:
        channel = ctx.message.author.voice.channel          #Finding the user's voice channel
        voice = get(client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():                  #If the bot is on another voice channel, it will move in to the user's voice channel instead
            await voice.move_to(channel)
            await ctx.send(f"I moved to {channel}!")
        else:
            voice = await channel.connect()                 #If the bot is not on any voice channel, it will connect to the user's voice channel
            print(f"Bot has connected to {channel}\n")
            await ctx.send(f"I connected to {channel}!")
    except:
        await ctx.send("You are not in a voice channel!")   #Response that is sent if the user is not on a voice channel

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@client.command(pass_context=True, brief='Makes the bot leave any voice channel it is in currently.', description='Will force the bot to leave any voice channel it is in currently. User does not need to be in the same voice channel as the bot when entering this command.')
async def leave(ctx):   #LEAVE COMMAND --- !leave
    voice = ctx.message.guild.voice_client
    try:
        if voice and voice.is_connected():
            await voice.disconnect()                        #Disconnects the bot from the voice channel
            channel = ctx.message.author.voice.channel
            print(f"Bot has left {channel}\n")
            await ctx.send(f"I left {channel}!")
        else:
            print("Bot was told to leave voice channel, but was not in one")
            await ctx.send("Don't think I am in a voice channel!")
    except:
        await voice.disconnect()
        await ctx.send("I left all voice channels!")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@client.command(pass_context=True, brief='Pauses the current song.', description='Pauses the song at the moment the command was entered. The song can be resumed back from the same moment by typing !resume.')
async def pause(ctx):   #PAUSE COMMAND --- !pause
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():                        #If a song is playing...
        print("Music paused")
        voice.pause()                                       #Forces the song to pause
        await ctx.send(f"Music paused!")
    else:
        print("Music failed to pause")
        if voice and voice.is_paused():
            await ctx.send("Music is already paused! Type !resume to continue playback!")
        else:
            await ctx.send("Music not playing, could not pause!")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@client.command(pass_context=True, brief='Resumes the current song.', description='Used to resume a paused song. Type !pause to pause the currently playing song and then use !resume to resume it back to playing from where it was paused.')
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_paused():                         #If a song is paused...
        print("Music resumed")
        voice.resume()                                      #Forces song to resume
        await ctx.send(f"Music resumed!")
    else:
        print("Music could not be resumed")
        if voice and voice.is_playing():
            await ctx.send("Music is already playing!")
        else:
            await ctx.send("No songs are currently paused!")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@client.command(pass_context=True, brief='Skips the current song.', description='Skips the currently playing song and automatically plays the next queued song if there are any. Also lets the user know how many songs there are queued at the moment.')
async def skip(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    queues.clear()
    try:
        if voice and voice.is_playing():                                                #If a song is playing...
            DIR = os.path.abspath(os.path.realpath("Queue"))                            #Path for 'Queue' folder
            length = len(os.listdir(DIR))                                               #The number of files inside the 'Queue' folder
            still_queue = length - 1                                                    #-1 because the queue number needs to go down by 1 on each !skip
            if still_queue <= 0:
                voice.stop()                                                            #"skips" the song
                await ctx.send(f"Music skipped, no more song(s) left in the queue!")
            else:
                print("Music stopped")
                voice.stop()
                await ctx.send(f"Music skipped, {still_queue} song(s) left in the queue!")
        else:
            print("Music failed to skip")
            await ctx.send("Music not playing, could not skip!")
    except:
        voice.stop()
        await ctx.send(f"Music skipped, 0 song(s) left in the queue!")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

queues = {} #Empty object needed for queueing functionality

@client.command(pass_context=True, brief='Plays songs on the same voice channel as the user.', description='Can be used to play the sound of any YouTube video on the same voice channel as the user. If there is already a song playing, the user can queue songs to be played later instead, when the current song has ended.')
async def play(ctx, url: str):
    try:
        channel = ctx.message.author.voice.channel                  #Message author's voice channel
        voice = get(client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():                          #If bot is on a channel already...
            await voice.move_to(channel)                            #Forces bot to move onto to the message author's channel
        else:                                                       #In case the bot is not on a channel...
            voice = await channel.connect()                         #Forces bot to connect onto the message author's channel
            print(f"Bot has connected to {channel}\n")
            await ctx.send(f"Bot joined {channel}")
    except:
        await ctx.send(f"No users in any of the voice channels!")   #In case the user is not a voice channel
        return
    
    Queue_infile = os.path.isdir("./Queue")                         #Checking for 'Queue' folder
    if Queue_infile is False:                                       #If 'Queue' folder does not exist...
        os.mkdir("Queue")                                           #Will create a folder called 'Queue'
    DIR = os.path.abspath(os.path.realpath("Queue"))                #The path for the 'Queue' folder
    queue_size = len(os.listdir(DIR))                               #Number of files inside of 'Queue' folder
    queue_size += 1                                                 #Increase size number by 1
    add_queue = True                                                #add_queue "state" is set to True
    while add_queue:                            #Loops until add_queue is False
        if queue_size in queues:                #If queue_size is in queues...
            queue_size += 1                     #queue_size is increased by one
        else:                                   #In case queue_size in queues returns False...
            add_queue = False                   #add_queue "state" is set to False
            queues[queue_size] = queue_size

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{queue_size}.%(ext)s")  #Location and naming the files that are to be queued

    ydl_opts = {                        #Download configurations for youtube_dl
        'format': 'bestaudio/best',
        'outtmpl': queue_path,          #Designating queue_path as the output template
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',    #Format - mp3
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading song...\n")
        ydl.download([url])             #Downloads song using ydl_opts
    
    if voice and voice.is_playing():    #If a song is already playing...
        await ctx.send("A song is already playing, added into a queue instead!")
    else:                               #In case a song is not playing
        await ctx.send("Playing song!")
    
    print("Song added to queue\n")

    def check_queue():          #Function to check current queue
        Queue_infile = os.path.isdir("./Queue")     #Checking for 'Queue' folder
        if Queue_infile is True:                    #If 'Queue' folder exists
            DIR = os.path.abspath(os.path.realpath("Queue"))    #Getting path for 'Queue' folder
            length = len(os.listdir(DIR))           #Number of files inside of 'Queue'
            still_queue = length - 1                #-1 length because we are getting a new song again
            try:
                first_file = os.listdir(DIR)[0]     #Getting first file in 'Queue' folder
            except:
                print("No more queued songs")
                queues.clear()                      #In case no more files exist in 'Queue' folder
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)  #Location of the file inside of 'Queue'
            if length != 0:                         #In case the number of files in 'Queue' is anything other than 0...
                print("Song done, playing next queued song\n")
                print(f"Songs still in queue: {still_queue}")
                ctx.send(f"Number of songs still in queue: {still_queue}")
                song_is_there = os.path.isfile("song.mp3")  #Checking for a file called 'song.mp3' - returns either True or False
                if song_is_there:                           #If 'song.mp3' is there...
                    os.remove("song.mp3")               #Old song file is removed
                shutil.move(song_path, main_location)   #New song is moved from 'Queue' onto root
                for file in os.listdir("./"):       #For every file in "./" (root)...
                    if file.endswith(".mp3"):       #If file endswith .mp3 - checking for the newly moved song file
                        #name = file
                        os.rename(file, 'song.mp3') #Song is renamed to 'song.mp3' which voice.play() method can play

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())   #Plays song on voice channel, re-runs check_queue()-function afterwards
                voice.source = discord.PCMVolumeTransformer(voice.source)                       #Source
                voice.source.volume = 0.25                                                      #Volume

                #newname = name.rsplit("-", 2)
                #ctx.send(f"Playing: {newname[0]}")
                #print("Playing")

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("No songs were queued during the previous song\n")

    check_queue()   #Runs check_queue()-function

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@client.command(pass_context=True, brief='Used to check the size of the song queue.', description='Tells user the amount of songs that are currently queued to be played.')
async def queue(ctx):
    try:
        DIR = os.path.abspath(os.path.realpath("Queue"))            #Checking path to 'Queue' folder
    length = len(os.listdir(DIR))                                   #Number of files inside of 'Queue' folder
        await ctx.send(f"{length} song(s) currently in queue!")
    except:
        await ctx.send("0 song(s) currently in queue!")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await client.process_commands(message)      #Needed for @client.commands to work

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

client.run(token)                               #Runs the bot with the token