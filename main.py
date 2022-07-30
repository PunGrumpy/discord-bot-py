import discord
import discord.ext
import configs

from blessed import Terminal
from discord.ext import commands

# SETUP DISCORD #
client = discord.Client()

client = commands.Bot(command_prefix="!",
                      intents=discord.Intents.all(),
                      help_command=None)

t = Terminal()

# Cogs
initial_extensions = [
                        'cogs.ready', 
                        'cogs.moderation', 
                        'cogs.auto_moderation',
                        'cogs.fun', 
                        'cogs.general', 
                        'cogs.help', 
                        'cogs.info', 
                        'cogs.status', 
                    ]

for extension in initial_extensions:
        try:
            client.load_extension(extension)
            print(t.green(f'Load {extension} successed!'))
        except Exception as e:
            print(e)

# Auto add role
@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='DISCIPLES')
    await member.add_roles(role)


token = configs.DISCORD_TOKEN
client.run(token)
