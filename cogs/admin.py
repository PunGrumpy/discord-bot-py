import discord
import discord.ext
import os
import configs
import asyncio
import subprocess

from discord.ext.commands import Bot, Cog
from discord.commands import (
    slash_command,
    Option
)

cogs = [file.replace(".py", "") for file in os.listdir("cogs") if file.endswith(".py")]

class Admin(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def run_process(self, command: str) -> list[str]:
        try:
            process = await asyncio.create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = await process.communicate()
        except NotImplementedError:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = await self.bot.loop.run_in_executor(None, process.communicate)

        return [output.decode() for output in result]

    # Reload cogs
    @slash_command(
        name="reload-cogs",
        description="Reload cogs or all cogs",
        options=[
            Option(
                name="cog",
                description="The cog to reload",
                required=True,
                type=3,
                choices=cogs
            )
        ]
    )
    async def reload_cogs(self, ctx, cog):
        """Reload cogs or all cogs"""
        if ctx.author.id != int(configs.OWNER_ID):
            embed = discord.Embed(title="Error", description="You are not the owner", color=discord.Color.red())
            await ctx.respond(embed=embed, ephemeral=True)
            return
        try:
            if cog == "all":
                for filename in os.listdir("./cogs"):
                    if filename.endswith(".py"):
                        self.bot.reload_extension(f"cogs.{filename[:-3]}")
                embed = discord.Embed(title="Success", description="Reloaded all cogs", color=discord.Color.green())
                await ctx.respond(embed=embed, ephemeral=True)
            else:
                self.bot.reload_extension(f"cogs.{cog}")
                embed = discord.Embed(title="Success", description=f"Reloaded {cog}", color=discord.Color.green())
                await ctx.respond(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(title="Error", description=f"{e}", color=discord.Color.red())
            await ctx.respond(embed=embed, ephemeral=True)

    # Load cogs
    @slash_command(
        name="load-cogs",
        description="Load cogs or all cogs",
        options=[
            Option(
                name="cog",
                description="The cog to load",
                required=True,
                type=3,
                choices=cogs
            )
        ],
    )
    async def load_cogs(self, ctx, cog):
        """Load cogs or all cogs"""
        if ctx.author.id != int(configs.OWNER_ID):
            embed = discord.Embed(title="Error", description="You are not the owner", color=discord.Color.red())
            await ctx.respond(embed=embed, ephemeral=True)
            return
        if cog == "all":
            for filename in os.listdir("./cogs"):
                if filename.endswith(".py"):
                    self.bot.load_extension(f"cogs.{filename[:-3]}")
            embed = discord.Embed(title="Success", description="Loaded all cogs", color=discord.Color.green())
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            try:
                self.bot.load_extension(f"cogs.{cog}")
                embed = discord.Embed(title="Success", description=f"Loaded {cog}", color=discord.Color.green())
                await ctx.respond(embed=embed, ephemeral=True)
            except Exception as e:
                embed = discord.Embed(title="Error", description=f"{e}", color=discord.Color.red())
                await ctx.respond(embed=embed, ephemeral=True)

    # Unload cogs
    @slash_command(
        name="unload-cogs",
        description="Unload cogs or all cogs",
        options=[
            Option(
                name="cog",
                description="The cog to unload",
                required=True,
                type=3,
                choices=cogs
            )
        ],
    )
    async def unload_cogs(self, ctx, cog):
        """Unload cogs or all cogs"""
        if ctx.author.id != int(configs.OWNER_ID):
            embed = discord.Embed(title="Error", description="You are not the owner", color=discord.Color.red())
            await ctx.respond(embed=embed, ephemeral=True)
            return
        if cog == "all":
            for filename in os.listdir("./cogs"):
                if filename.endswith(".py"):
                    self.bot.unload_extension(f"cogs.{filename[:-3]}")
            embed = discord.Embed(title="Success", description="Unloaded all cogs", color=discord.Color.green())
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            try:
                self.bot.unload_extension(f"cogs.{cog}")
                embed = discord.Embed(title="Success", description=f"Unloaded {cog}", color=discord.Color.green())
                await ctx.respond(embed=embed, ephemeral=True)
            except Exception as e:
                embed = discord.Embed(title="Error", description=f"{e}", color=discord.Color.red())
                await ctx.respond(embed=embed, ephemeral=True)                  

    # Shell command execution
    @slash_command(
        name="shell",
        description="Execute a shell command",
        option=[
            Option(
                name="command",
                description="The command to execute",
                required=True,
                type=3
            )
        ]
    )
    async def shell(self, ctx, command):
        """Execute a shell command"""
        if ctx.author.id != int(configs.OWNER_ID):
            embed = discord.Embed(title="Error", description="You are not the owner", color=discord.Color.red())
            await ctx.respond(embed=embed, ephemeral=True)
            return
        
        async with ctx.typing():
            stdout, stderr = await self.run_process(command)

        stdout, stderr = await self.run_process(command)
        if stderr:
            title = "Error"
            text = f'stdout:\n{stdout}\nstderr:\n{stderr}'
            color = discord.Color.red()
        else:
            title = "Success"
            text = stdout
            color = discord.Color.green()
        embed = discord.Embed(title=title, description=f"Executed command `{command}`", color=color)
        embed.add_field(name="Stdout", value=f"```{text}```", inline=False)                    
        await ctx.respond(embed=embed, ephemeral=True)

    # Restart the bot & show command for owner only
    @slash_command(
        name="restart",
        description="Restart the bot"
    )
    @commands.is_owner()
    async def restart(self, ctx):
        """Restart the bot"""
        if ctx.author.id != int(configs.OWNER_ID):
            embed = discord.Embed(title="Error", description="You are not the owner", color=discord.Color.red())
            await ctx.respond(embed=embed, ephemeral=True)
            return
        embed = discord.Embed(title="Success", description="Restarting bot", color=discord.Color.green())
        await ctx.respond(embed=embed, ephemeral=True)
        await self.bot.close()

def setup(bot: Bot):
    bot.add_cog(Admin(bot))