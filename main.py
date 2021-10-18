import discord
import os
TOKEN = os.environ['TOKEN']
import asyncio
from threading import Thread
from commands import r, qm, start, redirect, help
from keep_alive import keep_alive
from replit import db

client = discord.Client()

pouce=False
more= False
answered=[]


teams=["TEAM 1", "TEAM 2", "TEAM 3", "TEAM 4"]

@client.event
async def on_ready():
  print('I am {0.user}'.format(client))
  act= discord.Activity(type= discord.ActivityType.watching,name='Quiz in Servers') 
  await client.change_presence(status=discord.Status.online
  , activity=act)
@client.event
async def on_message(message):
  quizmaster= False
  if message.author == client.user:
    return
    global pouce, more, answered
    
  if pouce==True:
    ch= client.get_channel(int(db["qmchannel"]))
    cate= client.get_channel(message.channel.category_id)
    if str(cate) in teams:
      answered.append(str(cate))
      if answered.count(str(cate))==1:
        await ch.send(db["sqm"]+"\nAnswer: **"+str(message.content)+"**\nBy "+message.author.name + " for **"+str(cate)+"**")
      
        
        more= False
        await message.channel.send(message.author.mention+" Your answer **"+ message.content+ "** has been considered.")
      else:
        await message.channel.send("Already Pounced")
  
  sqmbool= False
  msg = message.content
  # global sqmbool
  try:

    qmroleid= db["sqm"]
    qmroleid = qmroleid.split("<@&",1)[1]
    qmroleid= qmroleid[:-1]
    if qmroleid in str(message.author.roles):
      # global quizmaster
      quizmaster= True
  except Exception as e:
    await message.channel.send("No quizmaster is set till now")
    sqmbool= True
    print(e)
  # quizmaster= True
    

  if msg.startswith('.'):
    command= msg.split(".",1)[1]
    command= command.lstrip()
    if command.startswith("b")&quizmaster:
      line= command.split("b", 1)[1]
      await r(client, message, line)
    if command.startswith("qm"):
      await qm(client, message)
    if command.startswith("start")&quizmaster:
      answered=[]
      try:
        pouce=True
        
        timed= command.split("start ", 1)[1]
        t= Thread(target=await start(client, message, int(timed)-1))
        
        t.start()
        await asyncio.sleep(int(timed)-1)
        pouce=False
        
      except:
        pouce= True
        t= Thread(target=await start(client, message, 20))
        t.start()
        await asyncio.sleep(20)
        pouce=False
        
    if command.startswith("redirect")&quizmaster:
      await redirect(client, message,  command) 
    if command.startswith("sqm"):
      if quizmaster|sqmbool:
        role= command.split("sqm ",1)[1]
        db["sqm"]=str(role)
        await message.channel.send("Done!")
    if command.startswith("hi"):
      await help(message, discord)
      # role= role.split("<@&", 1)[1]
      # role= role[:-1]
      # client.get(message.server.roles, id=role)

     
      
keep_alive()
client.run(TOKEN)
