import discord
import discord.ext
import configs
import os

from blessed import Terminal
from discord.ext import commands, tasks

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

@tasks.loop(seconds=0.5)
async def update_database_loop():
    configs.update_database()
    configs.BAD_WORD = [word['badword'] for word in configs.db_words.find()]
    configs.SPAM_LINK = [link['spamlink'] for link in configs.db_links.find()]

update_database_loop.start()
token = configs.DISCORD_TOKEN
client.run(token)
