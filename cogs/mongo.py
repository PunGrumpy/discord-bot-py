import discord
import discord.ext
import pymongo
import configs

from discord.ext import tasks
from discord.ext.commands import Bot, Cog, has_permissions
from discord.commands import (
    slash_command,
    Option
)

class Mongo(Cog):
    def __init__(self, bot):
        self.bot = bot

    # MongoDB Status
    @slash_command(
        name="mongo-status",
        description="Check the status of the MongoDB database.",
    )
    @has_permissions(administrator=True)
    async def mongo_status(self, ctx):
        """Check the status of the MongoDB database."""
        if(ctx.author.id != int(configs.OWNER_ID)):
            return await ctx.respond("You do not have permission to use this command.", ephemeral=True)
        try:
            configs.client.server_info()
            embed = discord.Embed(title="MongoDB Status", description=f"The MongoDB database is online. **{round(configs.client.server_info()['ok'])} ms**", color=0x00ff00)
            await ctx.respond(embed=embed)
        except pymongo.errors.ServerSelectionTimeoutError:
            embed = discord.Embed(title="MongoDB Status", description="The MongoDB database is offline.", color=0xff0000)
            await ctx.respond(embed=embed)

    # MongoDB View
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
    async def mongo_view(self, ctx, collection):
        """View all bad words or all spam links in the database."""
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

    @slash_command(
        name="mongo-add",
        description="Add a bad word or a spam link to the database.",
        options=[
            Option(
                name="collection",
                description="The type of data to add.",
                required=True,
                type=3,
                choices=[
                    "Bad Words",
                    "Spam Links"
                ]
            ),
            Option(
                name="data",
                description="The data to add.",
                required=True,
                type=3
            )
        ]
    )
    @has_permissions(administrator=True)
    async def mongo_add(self, ctx, collection, data):
        """Add a bad word or a spam link to the database."""
        if(ctx.author.id != int(configs.OWNER_ID)):
            return await ctx.respond("You do not have permission to use this command.", ephemeral=True)
        if(collection == "Bad Words"):
            if(configs.db_words.find_one({"badword": data})):
                return await ctx.respond("This bad word already exists in the database.", ephemeral=True)
            configs.db_words.insert_one({"badword": data})
            configs.BAD_WORD = [word['badword'] for word in configs.db_words.find()]
            await ctx.respond(f"Successfully added `{data}` to the database.", ephemeral=True)
        elif(collection == "Spam Links"):
            if(configs.db_links.find_one({"spamlink": data})):
                return await ctx.respond("This spam link already exists in the database.", ephemeral=True)
            configs.db_links.insert_one({"spamlink": data})
            configs.SPAM_LINK = [link['spamlink'] for link in configs.db_links.find()]
            await ctx.respond(f"Successfully added `{data}` to the database.", ephemeral=True)
        else:
            await ctx.respond("Invalid collection or Something went wrong...", ephemeral=True)

    # MongoDB Remove
    @slash_command(
        name="mongo-remove",
        description="Remove a bad word or a spam link from the database.",
        options=[
            Option(
                name="collection",
                description="The type of data to remove.",
                required=True,
                type=3,
                choices=[
                    "Bad Words",
                    "Spam Links"
                ]
            ),
            Option(
                name="data",
                description="The data to remove.",
                required=True,
                type=3
            )
        ]
    )
    @has_permissions(administrator=True)
    async def mongo_remove(self, ctx, collection, data):
        """Remove a bad word or a spam link from the database."""
        if(ctx.author.id != int(configs.OWNER_ID)):
            return await ctx.respond("You do not have permission to use this command.", ephemeral=True)
        if(collection == "Bad Words"):
            if(not configs.db_words.find_one({"badword": data})):
                return await ctx.respond("This bad word does not exist in the database.", ephemeral=True)
            configs.db_words.delete_one({"badword": data})
            configs.BAD_WORD = [word['badword'] for word in configs.db_words.find()]
            await ctx.respond(f"Successfully removed `{data}` from the database.", ephemeral=True)
        elif(collection == "Spam Links"):
            if(not configs.db_links.find_one({"spamlink": data})):
                return await ctx.respond("This spam link does not exist in the database.", ephemeral=True)
            configs.db_links.delete_one({"spamlink": data})
            configs.SPAM_LINK = [link['spamlink'] for link in configs.db_links.find()]
            await ctx.respond(f"Successfully removed `{data}` from the database.", ephemeral=True)
        else:
            await ctx.respond("Invalid collection or Something went wrong...", ephemeral=True)

    # MongoDB Update
    @slash_command(
        name="mongo-update",
        description="Update a bad word or a spam link in the database.",
        options=[
            Option(
                name="collection",
                description="The type of data to update.",
                required=True,
                type=3,
                choices=[
                    "Bad Words",
                    "Spam Links"
                ]
            ),
            Option(
                name="old_data",
                description="The old data to update.",
                required=True,
                type=3
            ),
            Option(
                name="new_data",
                description="The new data to update.",
                required=True,
                type=3
            )
        ]
    )
    @has_permissions(administrator=True)
    async def mongo_update(self, ctx, collection, old_data, new_data):
        """Update a bad word or a spam link in the database."""
        if(ctx.author.id != int(configs.OWNER_ID)):
            return await ctx.respond("You do not have permission to use this command.", ephemeral=True)
        if(collection == "Bad Words"):
            if(not configs.db_words.find_one({"badword": old_data})):
                return await ctx.respond("This bad word does not exist in the database.", ephemeral=True)
            configs.db_words.update_one({"badword": old_data}, {"$set": {"badword": new_data}})
            configs.BAD_WORD = [word['badword'] for word in configs.db_words.find()]
            await ctx.respond(f"Successfully updated `{old_data}` to `{new_data}` in the database.", ephemeral=True)
        elif(collection == "Spam Links"):
            if(not configs.db_links.find_one({"spamlink": old_data})):
                return await ctx.respond("This spam link does not exist in the database.", ephemeral=True)
            configs.db_links.update_one({"spamlink": old_data}, {"$set": {"spamlink": new_data}})
            configs.SPAM_LINK = [link['spamlink'] for link in configs.db_links.find()]
            await ctx.respond(f"Successfully updated `{old_data}` to `{new_data}` in the database.", ephemeral=True)
        else:
            await ctx.respond("Invalid collection or Something went wrong...", ephemeral=True)

def setup(bot):
    bot.add_cog(Mongo(bot))