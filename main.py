import discord
import os
import datetime

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)



reminders = {}

def gen_resp(message):
    return message.content.split(" ", 1)[1]

def splittime(message):
        try:
            text = message.content.split(" ", 3)
            text.append("No text set")
            time = text[1] + " " + text[2]
            text = text[3]
            time = datetime.datetime.strptime(time, '%m/%d/%y %H:%M:%S')
            return time, text
        except:
            return None, None
        
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
        time, text = splittime(message)
        if time == None or text == None:
            message.channel.send("The format is $setreminder MM/DD/YYYY HH:MM:SS reason", reference = message)
            return
        userid = message.author.id
        if(userid not in reminders):
            reminders[userid] = []
        reminders[userid].append([time, text])
        await message.channel.send("reminder set", reference = message)

    
    elif message.content.startswith("delreminder"):
        return
    
    elif message.content.startswith("$myreminders"):
        userid = message.author.id
        if(userid not in reminders):
            await message.channel.send("You havent set any reminders", reference = message)
            return
        i = 1
        mes = ""
        for time, text in reminders[userid]:
            mes = mes+f"{i}) {time} {text}\n"
            i = i + 1
        await message.channel.send(mes, reference = message)
