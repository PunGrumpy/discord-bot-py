import discord
import discord.ext
import configs

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
    'cogs.moderation', 
    'cogs.auto_moderation',
    'cogs.fun', 
    'cogs.general', 
    'cogs.help', 
    'cogs.info', 
    'cogs.status', 
    'cogs.mongo',
    'cogs.admin',
]

for extension in initial_extensions:
    try:
        client.load_extension(extension)
        print(t.green(f'Load {extension} successed!'))
    except Exception as e:
        print(e)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="𝐇 𝐄 𝐋 𝐋"))
    print()
    print(t.green(f'Successfully logged in.'))
    print(t.black(f'—————————————————————————————————'))
    print(t.white(f'Username : ') + t.red(f"{client.user.name}"))
    print(t.white(f'ID : ') + t.red(f"{client.user.id}"))
    print(t.white(f'Command prefix : ') + t.red("!"))
    print(t.white(f'Guilds count : ') + t.red(f"{len(client.guilds)}"))
    print(t.black(f'—————————————————————————————————'))
    print(t.grey(f'Discord Version : ') + t.white(f"{discord.__version__}"))
    print(t.black(f'—————————————————————————————————'))

token = configs.DISCORD_TOKEN
client.run(token)
