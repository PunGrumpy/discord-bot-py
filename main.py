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
    client = configs.client
    db = client['discord']
    db_words = db['words']
    db_links = db['links']
    configs.BAD_WORD = [word['badword'] for word in db_words.find()]
    configs.SPAM_LINK = [link['spamlink'] for link in db_links.find()]

update_database_loop.start()
token = configs.DISCORD_TOKEN
client.run(token)
