import discord
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)



def gen_resp(message):
    return message.content.split(" ", 1)[1]

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.mentions:
        if len(message.mentions)> 1:
            return
        elif message.mentions[0].id != 1062387390716592189:
            return
        await message.channel.send(gen_resp(message), reference = message)
            #1062387390716592189
    elif message.content.startswith('$hello'):
        await message.channel.send('Hello!', reference = message)
        
    elif message.content.startswith("$setreminder"):
        return
    
    elif message.content.startswith("delreminder"):
        return
    
    elif message.content.startswith("$myreminders"):
        return
