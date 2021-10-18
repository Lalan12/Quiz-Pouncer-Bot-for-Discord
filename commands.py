import asyncio

from replit import db

async def r(client, message, line ):
      players=[]
  
      if line=="":
        msg_sent=await message.channel.send("React Now!!!")
        await msg_sent.add_reaction(emoji= "✋")
        await message.delete()
      else:
        msg_sent=await message.channel.send(line)
        await msg_sent.add_reaction(emoji= "✋")
        await message.delete()
      cache_msg = await message.channel.fetch_message(msg_sent.id)
      while len(players)<2:
        for reaction in cache_msg.reactions:
          if reaction.emoji == '✋':
              async for user in reaction.users():
                
                if user != client.user:
                  players.append(user.mention)

          if len(players) ==1:
            await message.channel.send(players[0]+" is the first to react")
            
          else:
            pass

async def qm(client, message):
  msg=message.content
  channel = msg.split(".qm ",1)[1]
  await message.channel.send(channel+" is the QuizMaster's channel now")
  channel= channel.split("<#",1)[1]
  db.set("qmchannel", channel[:-1])

  
  await message.delete()

async def start(client, message, timed):
  qc1= db["pchannel1"]
  qc2= db["pchannel2"]
  qc3= db["pchannel3"]
  qc4= db["pchannel4"]
  qmchannel= db["qmchannel"]
  qmchannel= client.get_channel(int(qmchannel))
  qc1= client.get_channel(int(qc1))
  qc2= client.get_channel(int(qc2))
  qc3= client.get_channel(int(qc3))
  qc4= client.get_channel(int(qc4))
  await qc1.send("**The timer has started\nPounce now!!!**")
  await qc2.send("**The timer has started\nPounce now!!!**")
  await qc3.send("**The timer has started\nPounce now!!!**")
  await qc4.send("**The timer has started\nPounce now!!!**")
  await asyncio.sleep(timed)
  await qc1.send("**Time's up**\nNo more Pounces will be considered.")
  await qc2.send("**Time's up**\nNo more Pounces will be considered.")
  await qc3.send("**Time's up**\nNo more Pounces will be considered.")
  await qc4.send("**Time's up**\nNo more Pounces will be considered.")
  await qmchannel.send("**Time's up**")

async def redirect(client,message, command):
      channels= command.split("redirect ",1)[1]
      channels=channels.split()
      pchan1= channels[0]
      pchan1= pchan1.split("<#",1)[1]
      db["pchannel1"]= pchan1[:-1]
      pchan1= client.get_channel(int(pchan1[:-1]))
      
      pchan2= channels[1]
      pchan2= pchan2.split("<#",1)[1]
      db["pchannel2"]= pchan2[:-1]
      pchan2= client.get_channel(int(pchan2[:-1]))
      
      pchan3 = channels[2]
      pchan3= pchan3.split("<#",1)[1]
      db["pchannel3"]= pchan3[:-1]
      pchan3= client.get_channel(int(pchan3[:-1]))
      
      pchan4 = channels[3]
      pchan4= pchan4.split("<#",1)[1]
      db["pchannel4"]= pchan4[:-1]
      pchan4= client.get_channel(int(pchan4[:-1]))
      
      
      await pchan1.send("Pounce here!!!") 
      await pchan2.send("Pounce here!!!")
      await pchan3.send("Pounce here!!!") 
      await pchan4.send("Pounce here!!!") 
      
async def help(message, discord):
  embedVar = discord.Embed(title="I am here to help you!", description="All commands", color=0x33FFD7)
  embedVar.add_field(name=".qm <#channel>", value="This command can be used to tell the bot which is group for quizMaster", inline=True)
  embedVar.add_field(name=".redirect <#channel> <#channel> <#channel> <#channel>", value="It is used to tell the bot which channels will be used by the players", inline=False)
  embedVar.add_field(name=".b", value="Can be used like pouncing to see who raises hand first.", inline=False)
  embedVar.add_field(name=".sqm <@role>", value="Give the role of the QuizMaster", inline=False)
  embedVar.add_field(name=".start <time>", value="To start Pouncing and see who answers first.\nGive the time in seconds and only integer value\n If time is not given the default time is 20 secs", inline=False)
  embedVar.add_field(name=".hi", value="To see this message again", inline=False)
  embedVar.add_field(name="End!!!", value="Ended!", inline=False)
  

  await message.channel.send(embed= embedVar)
