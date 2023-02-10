import discord
import discord.ext
import pymongo
import configs
import time

from discord.ext import tasks
from discord.ext.commands import Bot, Cog, has_permissions, is_owner
from discord.commands import (
    slash_command,
    Option
)
from pymongo import MongoClient

class Mongo(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="mongo-status",
        description="Check the status of the MongoDB database.",
    )
    @has_permissions(administrator=True)
    async def mongo_status(self, ctx):
        if(ctx.author.id != int(configs.OWNER_ID)):
            return await ctx.respond("You do not have permission to use this command.", ephemeral=True)
        try:
            configs.client.server_info()
            embed = discord.Embed(title="MongoDB Status", description=f"The MongoDB database is online. **{round(configs.client.server_info()['ok'])} ms**", color=0x00ff00)
            await ctx.respond(embed=embed)
        except pymongo.errors.ServerSelectionTimeoutError:
            embed = discord.Embed(title="MongoDB Status", description="The MongoDB database is offline.", color=0xff0000)
            await ctx.respond(embed=embed)

    @slash_command(
        name="add-badword",
        description="Add a bad word to the database.",
        options=[
            Option(
                name="badword",
                description="The bad word to add to the database.",
                required=True,
                type=3
            )
        ]
    )
    @has_permissions(administrator=True)
    @is_owner()
    async def add_badword(self, ctx, badword):
        if(ctx.author.id != int(configs.OWNER_ID)):
            return await ctx.respond("You do not have permission to use this command.", ephemeral=True)
        if(configs.db_words.find_one({"badword": badword})):
            return await ctx.respond(f"The bad word **{badword}** already exists in the database.", ephemeral=True)
        configs.db_words.insert_one({"badword": badword})
        await ctx.respond(f"The bad word **{badword}** has been added to the database.", ephemeral=True)

    @slash_command(
        name="remove-badword",
        description="Remove a bad word from the database.",
        options=[
            Option(
                name="badword",
                description="The bad word to remove from the database.",
                required=True,
                type=3
            )
        ]
    )
    @has_permissions(administrator=True)
    @is_owner()
    async def remove_badword(self, ctx, badword):
        if(ctx.author.id != int(configs.OWNER_ID)):
            return await ctx.respond("You do not have permission to use this command.", ephemeral=True)
        if(not configs.db_words.find_one({"badword": badword})):
            return await ctx.respond(f"The bad word **{badword}** does not exist in the database.", ephemeral=True)
        configs.db_words.delete_one({"badword": badword})
        await ctx.respond(f"The bad word **{badword}** has been removed from the database.", ephemeral=True)

    @slash_command(
        name="mongo-view",
        description="View all bad words or all spam links in the database.",
        options=[
            Option(
                name="collection",
                description="The type of data to view.",
                required=True,
                type=3,
                choices=[
                    "Bad Words",
                    "Spam Links"
                ]
            )
        ]
    )
    @has_permissions(administrator=True)
    @is_owner()
    async def mongo_view(self, ctx, collection):
        if(ctx.author.id != int(configs.OWNER_ID)):
            return await ctx.respond("You do not have permission to use this command.", ephemeral=True)
        if(collection == "Bad Words"):
            data = [word['badword'] for word in configs.db_words.find()]
            if(len(data) == 0):
                return await ctx.respond("There are no bad words in the database.", ephemeral=True)
            await ctx.respond(f"`{data}`", ephemeral=True)
        elif(collection == "Spam Links"):
            data = [link['spamlink'] for link in configs.db_links.find()]
            if(len(data) == 0):
                return await ctx.respond("There are no spam links in the database.", ephemeral=True)
            await ctx.respond(f"`{data}`", ephemeral=True)
        else:
            await ctx.respond("Invalid collection or Something went wrong...", ephemeral=True)

def setup(bot):
    bot.add_cog(Mongo(bot))