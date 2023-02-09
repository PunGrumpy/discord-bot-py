import discord
import discord.ext
import configs
import os

from blessed import Terminal
from discord.ext import commands

# SETUP DISCORD
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
    'cogs.mongo',
]

for extension in initial_extensions:
    try:
        client.load_extension(extension)
        print(t.green(f'Load {extension} successed!'))
    except Exception as e:
        print(e)

token = configs.DISCORD_TOKEN
client.run(token)
