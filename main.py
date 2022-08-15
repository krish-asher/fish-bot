import discord
import json
from discord.ext import commands, tasks
from discord.utils import get
from discord import Member
import time
import requests

chanel_id = #################
client = commands.Bot(command_prefix="$",intents=discord.Intents.all())
client.remove_command('help')
#Events
@client.event
async def on_ready():
    print(f"we have logged in as {client.user}")
    del_old_requests.start()
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("$FISH BOT"))
    #check.start()
    #free_the_people.start()

@client.event
async def on_command_error(ctx,error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Pass in all required commands.")
  if isinstance(error, commands.CommandNotFound):
    await ctx.send("Invalid command")

@client.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass
    else:
        with open('react.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['message_id'] == payload.message_id and time.time()-x['time']<600:
                  if payload.emoji.name=='👍':
                    x['up-votes']+=1
                  if payload.emoji.name=='👎':
                    x['down-votes']+=1
                if time.time()-x['time']<600 and x['finished'] == False:
                  
                  person = discord.utils.get(client.get_guild(payload.guild_id).members, id=x['person'])

                  channel = discord.utils.get(client.get_guild(payload.guild_id).channels, id=chanel_id)

                  if x['role-id']==0:
                    if x['up-votes']-x['down-votes']>9:
                      invitelink = await channel.create_invite(max_uses=1,unique=True)
                      await person.send("You have been kicked")
                      await person.kick()
                      await channel.send(f"{person.mention} has been kicked")
                      x['finished'] = True


                  elif x['role-id']==1 and x['up-votes']-x['down-votes']>2:
                      await person.edit(mute = True)
                      await channel.send(f"{person.mention} is muted")
                      await person.send("You are muted")
                      x['finished'] = True

                  elif x['role-id']==2 and x['up-votes']-x['down-votes']>2:
                      await person.edit(mute = False)
                      await channel.send(f"{person.mention} is unmuted")
                      await person.send("You are unmuted")
                      x['finished'] = True
 
                  else:
                    if x['up-votes']-x['down-votes']>4:
                      role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role-id'])

                      if(x['type']):
                        await person.remove_roles(role)
                        x['finished'] = True
                        await channel.send(f"{person.mention} does not have {role} role")

                      else:
                        await person.add_roles(role)
                        x['finished'] = True
                        await channel.send(f"{person.mention} does have {role} role")

        with open('react.json', 'w') as f:
          json.dump(data, f, indent=4)

@client.event
async def on_raw_reaction_remove(payload):
        with open('react.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['message_id'] == payload.message_id and time.time()-x['time']<600:
                  if payload.emoji.name=='👍':
                    x['up-votes']-=1
                  if payload.emoji.name=='👎':
                    x['down-votes']-=1
                if time.time()-x['time']<600 and x['finished'] == False:              
                  person = discord.utils.get(client.get_guild(payload.guild_id).members, id=x['person'])

                  channel = discord.utils.get(client.get_guild(payload.guild_id).channels, id=chanel_id)

                  if x['role-id']==0:
                    if x['up-votes']-x['down-votes']>9:
                      await person.kick()
                      await channel.send(f"{rip.mention} has been kicked.")
                      x['finished'] = True


                  elif x['role-id']==1 and x['up-votes']-x['down-votes']>2:
                      await person.edit(mute = True)
                      await channel.send(f"{rip.mention} has been muted.")
                      await person.send("You are muted")
                      x['finished'] = True

                  elif x['role-id']==2 and x['up-votes']-x['down-votes']>2:
                      await person.edit(mute = False)
                      await channel.send(f"{rip.mention} is unmuted")
                      await person.send("You are unmuted")
                      x['finished'] = True
 
                  else:
                    if x['up-votes']-x['down-votes']>4:
                      role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role-id'])

                      if(x['type']):
                        await person.remove_roles(role)
                        x['finished'] = True
                        await channel.send(f"{person.mention} does not have {role} role")

                      else:
                        await rip.add_roles(role)
                        x['finished'] = True
                        x['time'] = time.time()
                        await channel.send(f"{person.mention} does not have {role} role")

        with open('react.json', 'w') as f:
          json.dump(data, f, indent=4)
"""
@client.event
async def on_member_update(before, after):
  with open('react.json') as react_file:
    data = json.load(react_file)
    game = [i for i in after.activities if str(i.type) == "ActivityType.playing"]
    if game:
      package = {
        'game': game[0].name,
        'person': after.id,
        'time': time.time(),
        'type': True
      }
      data.append(package)
  with open('react.json', 'w') as f:
    json.dump(data, f, indent=4)
"""
#Manage json
@tasks.loop(seconds=60)
async def del_old_requests():
  with open('react.json') as react_file:
    data = json.load(react_file)
    i=0
    while i < len(data):
      x = data[i]
      t = time.time()
      if t-x['time']>300:
        if(x['type']==False):
          role = discord.utils.get(client.get_guild(###################).roles, id=x['role-id'])
          person = discord.utils.get(client.get_guild(###################).members, id=x['person'])
          await person.remove_roles(role)
        del data[i]
        i-=1
      i+=1
  with open('react.json', 'w') as f:
    json.dump(data, f, indent=4)

"""
@tasks.loop(seconds=60)
async def check():
  channel = discord.utils.get(client.get_guild(##################).channels, id=chanel_id)
  with open('react.json') as react_file:
    data = json.load(react_file)
    for member in channel.members:
      x = member.activities
      if x:
        for i in x:
          if (str(i.type) == "ActivityType.playing"):
            if i.name != "/poll" and i.name != "$FISH BOT":
              sendInfo = {
                'person': member.id
                'game': i.name
                ''
              }
"""

#Commands
@client.command()
async def hello(ctx):
    await ctx.channel.send(f"Hello! {ctx.author.mention}")

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx,amount=5):
  await ctx.channel.purge(limit=amount+1)

@client.command()
async def unrevoke(ctx, user: discord.Member,*,message= ""):
  emb = discord.Embed(title = "Unrevoke", description=f"Do you want to unrevoke {user.mention}? \n {message}")
  print(ctx.channel)
  msg = await ctx.channel.send(embed=emb)
  await msg.add_reaction('👍')
  await msg.add_reaction('👎')
  with open('react.json') as json_file:
    data = json.load(json_file)

    new_react_role = {
      'role-id': ################, 
      'up-votes': 0,
      'down-votes': 0,
      'person': user.id,
      'message_id': msg.id,
      'time': time.time(),
      'type': True,
      'finished':False
    }
    data.append(new_react_role)
  with open('react.json', 'w') as f:
    json.dump(data, f, indent=4)

@client.command()
async def revoke(ctx, user: discord.Member,*, message = ""):
  emb = discord.Embed(title = "Revoke", description=f"Do you want to revoke {user.mention}? \n {message}")
  msg = await ctx.channel.send(embed=emb)
  await msg.add_reaction('👍')
  await msg.add_reaction('👎')
  with open('react.json') as json_file:
    data = json.load(json_file)

    new_react_role = {
      'role-id': ###############, 
      'up-votes': 0,
      'down-votes': 0,
      'person': user.id,
      'message_id': msg.id,
      'time': time.time(),
      'type': False,
      'finished':False
    }
    data.append(new_react_role)
  with open('react.json', 'w') as f:
    json.dump(data, f, indent=4)

@client.command()
async def kick(ctx, user:discord.Member,*,message=""):
  emb = discord.Embed(title = "Kick", description=f"Do you want to kick {user.mention}? \n \n{message}")
  msg = await ctx.channel.send(embed=emb)
  await msg.add_reaction('👍')
  await msg.add_reaction('👎')
  with open('react.json') as json_file:
    data = json.load(json_file)

    new_react_role = {
      'role-id': 0, 
      'up-votes': 0,
      'down-votes': 0,
      'person': user.id,
      'message_id': msg.id,
      'time': time.time(),
      'type': True,
      'finished':False
    }
    data.append(new_react_role)
  with open('react.json', 'w') as f:
    json.dump(data, f, indent=4)

@client.command()
async def mute(ctx, user: discord.Member,*,message=""):
  emb = discord.Embed(title = "Mute", description=f"Do you want to mute {user.mention}? \n \n{message}")
  msg = await ctx.channel.send(embed=emb)
  await msg.add_reaction('👍')
  await msg.add_reaction('👎')
  with open('react.json') as json_file:
    data = json.load(json_file)

    new_react_role = {
      'role-id': 1, 
      'up-votes': 0,
      'down-votes': 0,
      'person': user.id,
      'message_id': msg.id,
      'time': time.time(),
      'type': True,
      'finished':False
    }
    data.append(new_react_role)
  with open('react.json', 'w') as f:
    json.dump(data, f, indent=4)

@client.command()
async def unmute(ctx, user: discord.Member,*,message=""):
  emb = discord.Embed(title = "IUnmute", description=f"Do you want to unmute {user.mention}? \n \n{message}")
  msg = await ctx.channel.send(embed=emb)
  await msg.add_reaction('👍')
  await msg.add_reaction('👎')
  with open('react.json') as json_file:
    data = json.load(json_file)

    new_react_role = {
      'role-id': 2, 
      'up-votes': 0,
      'down-votes': 0,
      'person': user.id,
      'message_id': msg.id,
      'time': time.time(),
      'type': True,
      'finished':False
    }
    data.append(new_react_role)
  with open('react.json', 'w') as f:
    json.dump(data, f, indent=4)

@client.command()
async def free(ctx, user: discord.Member,*,message=""):
  with open('react.json') as react_file:
    data = json.load(react_file)
    found = False
    for x in data:
      if x['person'] == user.id:
        calc = (x['time']+300)-time.time()
        calc = calc//60
        await ctx.channel.send(f"{user.mention} has {calc} minutes left")
        found = True
    if found == False:
      await ctx.channel.send(f"{user.name} was not found.")
  with open('react.json', 'w') as f:
    json.dump(data, f, indent=4)

@client.command()
async def help(ctx):
  emb = discord.Embed(
    title = "Bot help",
    colour = discord.Colour.blue()
  )

  emb.add_field(name = "$revoke", value="Person loses the ability to send messages in channel if up votes minus down votes is greater than 5", inline=False)
  emb.add_field(name = "$unrevoke", value="Person gains the ability to send messages in channel if up votes minus down votes is greater than 5", inline=False)
  emb.add_field(name = "$kick", value="Person is kicked if up votes minus down votes is greater than 10", inline=False)
  emb.add_field(name = "$mute", value="Person is muted if up votes minus down votes is greater than 3", inline=False)
  emb.add_field(name = "$unmute", value="Person is unmuted if up votes minus down votes is greater than 3", inline=False)
  emb.add_field(name = "$free", value="Tells person how much time is left", inline=False)
  msg = await ctx.channel.send(embed=emb)

@client.command
async def AlwaysOnTheGame(ctx, user: discord.Member):
  await  ctx.send(user.status)

#TOKEN is a variable for the token of the bot which allows the bot to run this code.  Because this is public, I have not put it in.
client.run(TOKEN)

