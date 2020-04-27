import discord
import json
import random
import feedparser
import threading
import asyncio
import re

#Get token from file
f = open("data/token.data")
token = f.read().splitlines()[0]
f.close()

global prefix
prefix = ">"

global client
client = discord.Client()

async def whileLoop():
    while True:
        d = feedparser.parse("http://feeds.nightvalepresents.com/welcometonightvalepodcast")
        f = open("data/latestEp.data")
        latestEp = f.read()
        f.close()
        if d.entries[0].title not in latestEp:
            print("New Episode")
            desc = d.entries[0].description.splitlines()[0]
            cleanr = re.compile('<.*?>')
            cleantext = re.sub(cleanr, '', desc)
            print(cleantext)
            f = open("data/latestEp.data","w")
            f.write(d.entries[0].title)
            f.close()

            em = discord.Embed(title=d.entries[0].title,description=cleantext,colour=13124085)
            channel = client.get_channel(427145996284329985)
            await channel.send(embed=em)

        await asyncio.sleep(600)

async def cmd_ping(message):
    await message.channel.send("pong")

async def cmd_learn(message):
    msg = message.content.replace(f"{prefix}learn ","")
    trigger,action = msg.split("*")
    f = open("data/commands.json")
    commands = json.load(f)
    f.close()
    commands.update({trigger:action})
    f = open("data/commands.json","w")
    json.dump(commands,f)
    f.close()

    em = discord.Embed(title="Learn",colour=random.randint(0,16777215))
    em.add_field(name="Trigger",value=trigger,inline=False)
    em.add_field(name="Action",value=action,inline=False)
    await message.channel.send(embed=em)

async def cmd_unlearn(message):
    msg = message.content.replace(f"{prefix}unlearn ","")
    f = open("data/commands.json")
    commands = json.load(f)
    f.close()

    commands.pop(msg)
    f = open("data/commands.json","w")
    json.dump(commands,f)
    f.close()

    em = discord.Embed(title="Unlearn",description=msg,colour=random.randint(0,1677215))
    await message.channel.send(embed=em)

async def cmd_commands(message):
    f = open("data/commands.json")
    commands = json.load(f)
    f.close()

    em = discord.Embed(title="Commands",colour=random.randint(0,16777215))
    for i in commands:
        em.add_field(name=i,value=commands[i])

    await message.channel.send(embed=em)

@client.event
async def on_ready():
    global token
    del token
    print('Logged in as {0.user}'.format(client))
    await whileLoop()

@client.event
async def on_message(message):
    global prefix

    if message.author == client.user:
        return

    f = open("data/commands.json")
    commands = json.load(f)
    f.close()

    if message.content in commands:
        await message.channel.send(commands[message.content])

    if message.content.startswith(prefix):
        try:
            print("{} ({}) > {} ({}): {}".format(message.guild.name,message.guild.id,message.author.name,message.author.id,message.content))
        except:
            print("{} ({}): {}".format(message.author.name,message.author.id,message.content))
        msg = message.content.replace(prefix,"")
        try:
            msg,_ = msg.split(" ",1)
        except:
            msg = msg

        withoutPrefix = msg.replace(prefix,"")
        await globals()["cmd_{}".format(withoutPrefix)](message)

client.run(token)
