import discord
import os
import datetime
import asyncio


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
        
 async def remind_user():
    while True:
        print("running")
        current = datetime.datetime.now()
        for userid, reminder in reminders.items():
            for time, text in reminder:
                if current >=time:
                    user = await client.fetch_user(userid)
                    print(user)
                    await user.send(f"Reminder: {text}")
                    reminders[userid].remove([time, text])
        await asyncio.sleep(10)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await remind_user()

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

    
    elif message.content.startswith("$delreminder"):
        userid = message.author.id
        if(userid not in reminders):
            await message.channel.send("You havent set any reminders", reference = message)
            return
        elif len(message.content.split()) < 2:
            await message.channel.send("Specify the reminder index, you can check the index in $myreminders", reference = message)
            return
        elif (message.content.split()[1].isdigit() != True):
            await message.channel.send("format: $delreminder index(integer)", reference = message)
            return
        elif(int(message.content.split()[1])>=len(reminders[userid]) or int(message.content.split()[1])<=0):
            await message.channel.send("Reminder doesnt exist", reference = message)
            return
        reminders[userid].pop(int(message.content.split()[1])-1)
        await message.channel.send("Deleted reminder", reference = message)
    
    elif message.content.startswith("$myreminders"):
        userid = message.author.id
        if(userid not in reminders or reminders[userid] == []):
            await message.channel.send("You havent set any reminders", reference = message)
            return
        i = 1
        mes = ""
        for time, text in reminders[userid]:
            mes = mes+f"{i}) {time} {text}\n"
            i = i + 1
        await message.channel.send(mes, reference = message)
