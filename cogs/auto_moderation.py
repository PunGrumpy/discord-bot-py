import discord
import discord.ext
import datetime
import configs

from discord.ext.commands import Bot, Cog
from discord.ext import commands


class AutoMod(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Delete message auto
    @commands.Cog.listener()
    async def on_message(self, message):
        if(message.author.id == self.bot.user.id):
            return
        badwords = configs.BAD_WORD
        spamlink = configs.SPAM_LINK
            
        for bw in badwords:
            if bw in message.content:
                embed = discord.Embed(description=f"<a:alert:944877266402435092> reason : profanity word", color=discord.Color.red())
                embed.set_author(name=f'{message.author} has been warned', icon_url=message.author.avatar.url)
                await message.delete()
                await message.channel.send(embed=embed, delete_after=30)
                self.bot.dispatch("profanity", message, bw)
                return
        await self.bot.process_commands(message)

        for sl in spamlink:
            if sl in message.content:
                embed = discord.Embed(description=f"<a:alert:944877266402435092> reason : spam link", color=discord.Color.red())
                embed.set_author(name=f'{message.author} has been warned', icon_url=message.author.avatar.url)
                await message.delete()
                await message.channel.send(embed=embed, delete_after=30)
                self.bot.dispatch("spam", message, sl)
                return
        await self.bot.process_commands(message)

    # Logs
    @commands.Cog.listener()
    async def on_profanity(self, message, word):
        channel = discord.utils.get(message.guild.channels, name = configs.MOD_LOG_CHANNEL_NAME)
        
        embed = discord.Embed(title="Profanity Alert!", description=f"{message.author.mention} just said ||{word}||",color=0xff0000)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'{message.guild.name}', icon_url=message.guild.icon.url)
        await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_spam(self, message, word):
      channel = discord.utils.get(message.guild.channels, name = configs.MOD_LOG_CHANNEL_NAME)

      embed = discord.Embed(title="Spam Alert!", description=f"{message.author.mention} just said ||{word}||",color=0xff0000)
      embed.timestamp = datetime.datetime.utcnow()
      embed.set_footer(text=f'{message.guild.name}', icon_url=message.guild.icon.url)
      await channel.send(embed=embed)

def setup(bot: Bot):
    bot.add_cog(AutoMod(bot))
