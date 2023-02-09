import discord
import discord.ext
import pymongo
import configs

from discord.ext.commands import Bot, Cog, has_permissions
from discord.commands import (
    slash_command,
    Option
)
from pymongo import MongoClient

class Mongo(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = MongoClient(configs.MONGO_URL)

    @slash_command(
        name="mongo-status",
        description="Check the status of the MongoDB database.",
    )
    @has_permissions(administrator=True)
    async def mongo_status(self, ctx):
        if(ctx.author.id != int(configs.OWNER_ID)):
            return await ctx.respond("You do not have permission to use this command.", ephemeral=True)
        try:
            self.client.server_info()
            embed = discord.Embed(title="MongoDB Status", description="The MongoDB database is online.", color=0x00ff00)
            await ctx.respond(embed=embed)
        except pymongo.errors.ServerSelectionTimeoutError:
            embed = discord.Embed(title="MongoDB Status", description="The MongoDB database is offline.", color=0xff0000)
            await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Mongo(bot))
    