import discord
import discord.ext
import datetime
import time

from discord.ext.commands import Bot, Cog, has_permissions
from discord.commands import (
    slash_command,
    Option
)
from discord.ui import Button, View

class Confirm(discord.ui.View):
    def __init__(self, ctx):
        self.ctx = ctx
        super().__init__(timeout=10)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.ctx.author:
            return True
        await interaction.response.send_message("you can't do this", ephemeral=True)
        return False

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Ban Confirm", ephemeral=True)
        self.value = True
        time.sleep(1)
        await self.message.edit_original_response(view=None)
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Ban Cancel", ephemeral=True)
        self.value = False
        time.sleep(1)
        await self.message.edit_original_response(view=None)
        self.stop()
    
    async def on_timeout(self):
        if self.message:
            embedTimeout = discord.Embed(
                title="TIMEOUT",
                description=f"{self.ctx.author.mention} Cancelled, time out",
                color=discord.Color.dark_red())
            embedTimeout.set_footer(text=f'Requested by - {self.ctx.author}',
                                icon_url=self.ctx.author.avatar.url)
            embedTimeout.timestamp = datetime.datetime.utcnow()
            # self.button_1.disabled = True
            # self.myselect.disabled = True
            await self.message.edit_original_response(embed=embedTimeout, view=None)

class Moderation(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Clear
    @slash_command(
        name="clear", 
        description="Clear messages"
    )
    @has_permissions(manage_messages=True)
    async def clear(
        self, 
        ctx: discord.ApplicationContext,
        amount: Option(int, "Provide the amount of messages you want to delete", min_value=1, max_value=100)
    ):
        """Clear messages"""
        if (amount <= 100):
            embed = discord.Embed(title=f"Delete Message : {amount}",
                                  description="The message has been deleted.",
                                  color=0xff0000)
            embed.set_footer(text=f'Used by - {ctx.author}',
                             icon_url=ctx.author.avatar.url)
            await ctx.channel.purge(limit=amount)
            await ctx.respond(embed=embed, delete_after=5)
        elif (amount > 100):
            embed = discord.Embed(
                title="Error Amount",
                description="Change the amount. (amount <= 100)",
                color=0xff0000)
            embed.set_footer(text=f'Used by - {ctx.author}',
                             icon_url=ctx.author.avatar.url)
            await ctx.respond(embed=embed, delete_after=5)

    # Ban
    @slash_command(
        name="ban", 
        description="Ban someone user"
    )
    @has_permissions(ban_members=True)
    async def _ban(self,
                   ctx,
                   member: Option(discord.User, "The user you want to kick"),
                   reason: Option(str, "The reason you kicked the user", required=False)
    ):
        """Ban someone user"""
        if reason == None:
            reason = "No reason provided."

        embed = discord.Embed(
            title=f"<a:RinShockBlush:779719777148993568> BAN",
            description=
            f"Are you sure you want to ban {member.mention}? \n{ctx.author.mention} choose : (Y/N)",
            color=discord.Color.random())
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Requested by - {ctx.author}',
                         icon_url=ctx.author.avatar.url)
        view = Confirm(ctx)
        view.message = await ctx.respond(embed=embed, view=view)

        embedConfirm = discord.Embed(
            title="<a:shinobu_dan_ando:944946216540717136> BAN CONFIRMED",
            description=
            f"{member.mention} has been banned.\nreason : `{reason}`",
            color=discord.Color.green())
        embedConfirm.timestamp = datetime.datetime.utcnow()
        embedConfirm.set_footer(text=f'Requested by - {ctx.author}',
                                icon_url=ctx.author.avatar.url)
        embedCancel = discord.Embed(
            title="<a:PandaPingRee:944946496699265105> BAN CANCELLED",
            description=f"Ban {member.mention} has been cancelled.",
            color=discord.Color.red())
        embedCancel.timestamp = datetime.datetime.utcnow()
        embedCancel.set_footer(text=f'Requested by - {ctx.author}',
                               icon_url=ctx.author.avatar.url)
        embedTimeout = discord.Embed(
                title="TIMEOUT",
                description=f"{ctx.author.mention} Cancelled, time out",
                color=discord.Color.dark_red())
        embedTimeout.set_footer(text=f'Requested by - {ctx.author}',
                                icon_url=ctx.author.avatar.url)
        embedTimeout.timestamp = datetime.datetime.utcnow()

        await view.wait()
        if view.value is None:
            await ctx.interaction.edit_original_response(embed=embedTimeout)
            return
        elif view.value:
            await member.ban()
            await ctx.interaction.edit_original_response(embed=embedConfirm)
            return
        else:
            await ctx.interaction.edit_original_response(embed=embedCancel)
            return

    # Kick
    @slash_command(
        name="kick", 
        description="Kick someone user"
    )
    @has_permissions(kick_members=True)
    async def _kick(self,
                    ctx, 
                    member: Option(discord.User, "The user you want to ban"),
                    reason: Option(str, "The reason you banned the user", required=False)
    ):
        """Kick someone user"""
        if reason == None:
            reason = "No reason provided."

        embed = discord.Embed(
            title=f"<a:RinShockBlush:779719777148993568> Kick",
            description=
            f"Are you sure you want to kick {member.mention}? \n{ctx.author.mention} choose : (Y/N)",
            color=discord.Color.random())
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Requested by - {ctx.author}',
                         icon_url=ctx.author.avatar.url)
        view = Confirm(ctx)
        view.message = await ctx.respond(embed=embed, view=view)

        embedConfirm = discord.Embed(
            title="<a:shinobu_dan_ando:944946216540717136> KICK CONFIRMED",
            description=f"{member.mention} has been kicked.",
            color=discord.Color.green())
        embedConfirm.timestamp = datetime.datetime.utcnow()
        embedConfirm.set_footer(text=f'Requested by - {ctx.author}',
                                icon_url=ctx.author.avatar.url)
        embedCancel = discord.Embed(
            title="<a:PandaPingRee:944946496699265105> KICK CANCELLED",
            description=f"Kick {member.mention} has been cancelled.",
            color=discord.Color.red())
        embedCancel.timestamp = datetime.datetime.utcnow()
        embedCancel.set_footer(text=f'Requested by - {ctx.author}',
                               icon_url=ctx.author.avatar.url)
        embedTimeout = discord.Embed(
                title="TIMEOUT",
                description=f"{ctx.author.mention} Cancelled, time out",
                color=discord.Color.dark_red())
        embedTimeout.set_footer(text=f'Requested by - {ctx.author}',
                                icon_url=ctx.author.avatar.url)
        embedTimeout.timestamp = datetime.datetime.utcnow()

        await view.wait()
        if view.value is None:
            await ctx.interaction.edit_original_response(embed=embedTimeout)
            return
        elif view.value:
            await member.kick()
            await ctx.interaction.edit_original_response(embed=embedConfirm)
            return
        else:
            await ctx.interaction.edit_original_response(embed=embedCancel)
            return

def setup(bot: Bot):
    bot.add_cog(Moderation(bot))
