import nextcord
from nextcord.ext import commands
import os
import json
from nextcord.ext import menus
from nextcord.ext.commands import MissingRequiredArgument
from nextcord.ext.commands import CommandNotFound
from nextcord.ext.commands import MissingPermissions
from nextcord.ext.commands import errors 


intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True

def get_prefix(client, message):
    if not message.guild:
        return "tk"

    try:
        with open('./prefixes.json', "r") as f:
            prefixes = json.load(f)

        return prefixes[str(message.guild.id)]

    except nextcord.DiscordException:
        return "tk"

client = commands.Bot(command_prefix=get_prefix, case_insensitive=True, activity = nextcord.Game(name='| tkhelp'), intents = intents, help_command=None)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('You are missing a required part of command!')
    elif isinstance(error, CommandNotFound):
        await ctx.send('Command not found!')
    elif isinstance(error, MissingPermissions):   
        await ctx.send('You do not have permission to use this command!')
    else:
        await ctx.send('An error has occured!')
        print(error)
        return 

@client.event 
async def on_ready():
    print('Tktb is started and online') 

@client.command()
async def help(ctx):
    try:
        with open('./prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefix = prefixes[str(ctx.guild.id)]

        embed = nextcord.Embed(title='tktb help', description=f'commands list and general support', color=0xb12ef7)
        embed.add_field(name=f'{prefix}help', value='Shows this message', inline=False)
        embed.add_field(name=f'{prefix}setprefix', value=f'Changes the bot prefix for the server | ex: {prefix}setprefix tk', inline=False)
        embed.add_field(name=f'{prefix}setup', value=f'Sets/ changes ticket channels | ex: {prefix}setup [ticket channel id] [ticket log channel id]', inline=False)
        embed.add_field(name=f'{prefix}ticket', value=f'Creates a support ticket | ex: {prefix}ticket example issue', inline=False)
        av_url = 'https://cdn.discordapp.com/avatars/996778688735621260/dbfed53f1e26b3a288a140406d071ba7.png?size=1024'
        embed.set_thumbnail(url=av_url)
        
        await ctx.send(embed=embed)
    except:
        return


@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
      with open('./prefixes.json', 'r') as f:
        prefixes = json.load(f)

      prefix = prefixes[str(message.guild.id)]
      embed = nextcord.Embed(title='tktb', description=f'Current server prefix is \'{prefix}\' \nFor more, use the \'{prefix}help\' associated commands', color=0xb12ef7)
      av_url = 'https://cdn.discordapp.com/avatars/996778688735621260/dbfed53f1e26b3a288a140406d071ba7.png?size=1024'
      embed.set_thumbnail(url=av_url)
      embed.add_field(name="Invite me to your server!", value="[invite tktb here](https://discord.com/api/oauth2/authorize?client_id=996778688735621260&permissions=277025745920&scope=bot%20applications.commands)")
      await message.channel.send(embed=embed)
    await client.process_commands(message)

@client.event
async def on_guild_join(guild):
    
    with open('./prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = 'tk'

    with open('./prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('./prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('./prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.command(aliases=['prefix', 'sp', 'sprefix'])
@commands.has_permissions(administrator=True)
async def setprefix(ctx, prefix):
    if commands.has_permissions(administrator=True):
        with open('./prefixes.json', 'r') as f:
            prefixes = json.load(f)
    
        prefixes[str(ctx.guild.id)] = prefix
    
        with open('./prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        emoji = '<:ShieldCheck:996559064295284826>'
        embed = nextcord.Embed(description=f'{emoji} Prefix successfully changed to {prefix}', color=0xb12ef7)
        await ctx.channel.send(embed=embed)
    else:
        return

@client.command(aliases=['s', 'set'])
@commands.has_permissions(administrator=True)
async def setup(ctx, tk_channel_id, tk_logchannel_id):
  if commands.has_permissions(administrator=True):
    try:
        with open('./ticketchannels.json', 'r') as f:
            ticketchannels = json.load(f)    
            ticketchannels[str(ctx.guild.id)] = tk_channel_id
        with open('./ticketchannels.json', 'w') as f:
            json.dump(ticketchannels, f, indent=4)

        with open('./ticketlogs.json', 'r') as f:
            ticketlogs = json.load(f)    
            ticketlogs[str(ctx.guild.id)] = tk_logchannel_id
        with open('./ticketlogs.json', 'w') as f:
            json.dump(ticketlogs, f, indent=4)

        channel_l = ctx.guild.get_channel(int(tk_channel_id))
        channel_2 = ctx.guild.get_channel(int(tk_logchannel_id))
        if channel_l and channel_2:
            await ctx.send(f'Successfully set ticket channel to {channel_l.mention} and ticket review channel to {channel_2.mention}')
            return
        else:
            await ctx.send('Ticket channels not found')
            return
    except:
        await ctx.send('Ticket channels not found')
        return

class Buttons(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @nextcord.ui.button(label="Close Ticket",style=nextcord.ButtonStyle.gray)
    async def gray_button(self,button:nextcord.ui.Button,interaction:nextcord.Interaction):
        embed = nextcord.Embed(title='Ticket resolved! 🎉', description='This ticket has been resolved and the user who requested it is no longer in need of assistance. Thank you for using tktb!\n ', color=0xb12ef7)
        av_url = 'https://cdn.discordapp.com/avatars/996778688735621260/dbfed53f1e26b3a288a140406d071ba7.png?size=1024'
        embed.set_thumbnail(url=av_url)
        embed.add_field(name="Invite me to your server!", value="[invite tktb here](https://discord.com/api/oauth2/authorize?client_id=996778688735621260&permissions=277025745920&scope=bot%20applications.commands)")
        await interaction.response.edit_message(embed=embed)
    
@client.command(aliases=['t'])
async def ticket(ctx, *, issue):
  if ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.moderate_members:
        await ctx.send('I can\'t create tickets for administrators!')
        return
  with open('./ticketchannels.json', 'r') as f:
        ticketchannels = json.load(f)    
        ticket_channel = ticketchannels[str(ctx.guild.id)] 
        channel1 = client.get_channel(int(ticket_channel))
        if ctx.channel == channel1:
          await ctx.channel.purge(limit=1)
          channel = await ctx.author.create_dm()
          embed = nextcord.Embed(title=f'Ticket recieved! In: {ctx.guild}', description=f'Hi {ctx.author}!\n \nI have logged that you are currently having trouble with:\n\n\'{issue}\' \n \nSomeone will be with you shortly! \n \nThank you for your patience.', timestamp=ctx.message.created_at, color=0xb12ef7)
          embed.set_thumbnail(url=ctx.author.avatar)
          embed.add_field(name="Invite me to your server!", value="[invite tktb here](https://discord.com/api/oauth2/authorize?client_id=996778688735621260&permissions=277025745920&scope=bot%20applications.commands)")
          await channel.send(embed=embed)
        else:
          await ctx.channel.purge(limit=1)
          await ctx.send(f'Wrong channel! {channel1.mention} is the correct channel.', delete_after=7)
          
  with open('./ticketlogs.json', 'r') as f:
    if ctx.channel == channel1:
        ticketlogs = json.load(f)
        log_channel = ticketlogs[str(ctx.guild.id)]
        channel2 = client.get_channel(int(log_channel))
        if channel2:
          embed = nextcord.Embed(title=f'Ticket Recieved', description=f'Member: {ctx.author} is currently having trouble with \n \n\'{issue}\'\n \nThey are waiting for your response!\n \nTo close this ticket, please click the button below.\n ', timestamp=ctx.message.created_at, color=0xb12ef7)
          embed.set_thumbnail(url=ctx.author.avatar)
          await channel2.send(embed=embed,view=Buttons())
        else:
          await ctx.send(f'Log channel error. Please either setup your ticket log channel, or check to make sure you entered in the right channel id.', delete_after=7)
    else:
      return      

client.run(your token here)
