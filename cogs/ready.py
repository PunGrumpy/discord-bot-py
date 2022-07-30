import discord
import platform
import discord.ext
import os, psutil
import cpuinfo

from discord.ext import commands
from blessed import Terminal

t = Terminal()


class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        # process = psutil.Process(os.getpid())
        # memory = (process.memory_info().rss / 1024 / 1024)
        # memory_str = "{:.2f}".format(memory)
        # RAM = psutil.virtual_memory().percent
        # CPU = psutil.cpu_percent(10) # sec
        # CPUBRAND = cpuinfo.get_cpu_info()['brand_raw']

        await self.bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching, name="𝐇 𝐄 𝐋 𝐋"))
        print()
        print(t.green(f'Successfully logged in.'))
        print(t.black(f'—————————————————————————————————'))
        print(t.white(f'Username : ') + t.red(f"{self.bot.user.name}"))
        print(t.white(f'ID : ') + t.red(f"{self.bot.user.id}"))
        print(t.white(f'Command prefix : ') + t.red("!"))
        print(t.white(f'Guilds count : ') + t.red(f"{len(self.bot.guilds)}"))
        print(t.black(f'—————————————————————————————————'))
        print(
            t.grey(f'Discord Version : ') + t.white(f"{discord.__version__}"))
        # print(t.grey(f"Memory : ") + t.white(f"{memory_str}") + t.white(" MB"))
        # print(t.grey(f'RAM : ') + t.white(f'{RAM}') + t.white(" %"))
        # print(t.grey(f'CPU : ') + t.white(f'{CPU}') + t.white(" %"))
        # print(t.grey(f"CPU brand : ") + t.white(f'{CPUBRAND}'))
        # print(t.grey(f'Total CPU core : ') + t.white(f'{psutil.cpu_count(logical=True)}'))
        # print(
        #     t.grey(f"Running on : ") +
        #     t.white(f"{platform.system()}" +
        #             t.white(f" {platform.architecture()[0]}")))

def setup(bot):
    bot.add_cog(Ready(bot))
