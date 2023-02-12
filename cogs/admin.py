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

cogs = [
    "all",
    "admin",
    "mongo",
    "moderation",
    "auto_moderation",
    "fun",
    "general",
    "help",
    "info",
    "status"
]

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

    # Github pull
    @slash_command(
        name="github-pull",
        description="Pull from github"
    )
    async def pull(self, ctx):
        """Pull from github"""
        if ctx.author.id != int(configs.OWNER_ID):
            embed = discord.Embed(title="Error", description="You are not the owner", color=discord.Color.red())
            await ctx.respond(embed=embed, ephemeral=True)
            return
        try:
            embed = discord.Embed(title="Success", description="Pulled from github", color=discord.Color.green())
            await ctx.respond(embed=embed, ephemeral=True)
            os.system("git pull origin main")
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
        stdout, stderr = await self.run_process(command)
        text = stderr if stderr else stdout
        try:
            os.system(command)
            embed = discord.Embed(title="Success", description=f"Executed command `{command}`", color=discord.Color.green())
            embed.add_field(name="Stdout", value=f"```{text}```", inline=False)
            await ctx.respond(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(title="Error", description=f"{e}", color=discord.Color.red())
            embed.add_field(name="Stdout", value=f"```{text}```", inline=False)
            await ctx.respond(embed=embed, ephemeral=True)

    # Reload cogs
    @slash_command(
        name="reload-cogs",
        description="Reload all cogs",
        option=[
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
        """Reload all cogs"""
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
        description="Load all cogs",
        option=[
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
        """Load all cogs"""
        if ctx.author.id != int(configs.OWNER_ID):
            embed = discord.Embed(title="Error", description="You are not the owner", color=discord.Color.red())
            await ctx.respond(embed=embed, ephemeral=True)
            return
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
        description="Unload all cogs",
        option=[
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
        """Unload all cogs"""
        if ctx.author.id != int(configs.OWNER_ID):
            embed = discord.Embed(title="Error", description="You are not the owner", color=discord.Color.red())
            await ctx.respond(embed=embed, ephemeral=True)
            return
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            embed = discord.Embed(title="Success", description=f"Unloaded {cog}", color=discord.Color.green())
            await ctx.respond(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(title="Error", description=f"{e}", color=discord.Color.red())
            await ctx.respond(embed=embed, ephemeral=True)                    

def setup(bot: Bot):
    bot.add_cog(Admin(bot))