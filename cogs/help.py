import discord
import discord.ext
import time
import configs

from discord.ext import commands
from discord.ext.commands import Bot, Cog
from discord.commands import (
    slash_command,
    Option
)

from discord.ui import View

class DropDownMenu(discord.ui.View):
    @discord.ui.select(placeholder="Select Categories", min_values=1, max_values=1, options=[
        discord.SelectOption(label="Home", description="Homepage", emoji="<:Campus:919134908524400670>"),
        discord.SelectOption(label="General", description="General commands", emoji="🌍"),
        discord.SelectOption(label="Infomation", description="Information commands", emoji="📜"),
        discord.SelectOption(label="Fun", description="Fun commands", emoji="<a:PepeLmfaoooo:944951463640186950>"),
        discord.SelectOption(label="Moderation", description="Moderation commands", emoji="<:moderator:949328694856523846>"),
        # discord.SelectOption(label="Other", description="Other commands", emoji="<:discordemployee:946660767074230312>"),
    ])
    async def callback(self, select, interaction: discord.Interaction):
        banner = configs.BANNER_HELP_COMMANDS
        if select.values[0] == "Home":
            # Embed homepage
            embed_home = discord.Embed(
                title="📑 HELP MENU",
                description=f"<a:pin:949334222760456202> **Important Info**\n[Invite Bot MEPHISTO#1211](https://discord.com/oauth2/authorize?client_id=907184657668386836&permissions=8&scope=bot%20applications.commands)\n[Donate](https://ko-fi.com/mephistogrumpy)",
                color=0xDF0000)
            embed_home.set_footer(text="Select Other Help Categories", icon_url="https://cdn.discordapp.com/attachments/908053630425366538/936672413075251292/Mephisto_2.jpg")
            embed_home.set_image(url=banner)

            await interaction.response.edit_message(embed=embed_home)

        if select.values[0] == "General":
            # Embed general
            embed_general = discord.Embed(
                title=
                "<:mephisto:940249600969801748> **Mephisto General Commands**",
                color=0xFF0000)
            embed_general.add_field(
                name="`/ping`", 
                value="Return websocket ping", 
                inline=False)
            embed_general.add_field(
                name="`/invite`",
                value="Invite bot to your server", 
                inline=False)
            embed_general.add_field(
                name="`/weather-info [city]`",
                value="Tell us the weather of the city you want to know", 
                inline=False)
            embed_general.add_field(
                name="`/donut`",
                value="Send ASCII art donut spinning", 
                inline=False)
            embed_general.add_field(
                name="`/bitcoin`",
                value="Get the current price of bitcoin", 
                inline=False)
            embed_general.add_field(
                name="`/spotify-status [user]`",
                value="Shows the song the user is listening to",
                inline=False)
            embed_general.set_image(url=banner)

            await interaction.response.edit_message(embed=embed_general)
        
        if select.values[0] == "Infomation":
            # Embed info
            embed_info = discord.Embed(
                title="<:mephisto:940249600969801748> **Mephisto Infomation Commands**",
                color=0xBE0000)
            embed_info.add_field(
                name="`/user-info [user]`",
                value="Get a infomation someone",
                inline=False)
            embed_info.add_field(
                name="`/bot-info [user]`",
                value="Get information about Mephisto bot", 
                inline=False)
            embed_info.add_field(
                name="`/server-info`", 
                value="Server info", 
                inline=False)
            embed_info.set_image(url=banner)

            await interaction.response.edit_message(embed=embed_info)

        if select.values[0] == "Fun":
            # Embed fun
            embed_fun = discord.Embed(
                title="<:mephisto:940249600969801748> **Mephisto Fun Commands**",
                color=0x900000)
            embed_fun.add_field(name="`/joke`", value="Get a random joke", inline=False)
            embed_fun.add_field(name="`/meme`", value="Get a random meme", inline=False)
            embed_fun.add_field(name="`/gif`", value="Get GIF that you want", inline=False)
            embed_fun.add_field(name="`/nitro`", value="Send a totally not a scamming nitro message that totally would not hack a Discord Account!", inline=False)
            embed_fun.add_field(name="`/8ball [question]`", value="Ask a question to the 8ball", inline=False)
            embed_fun.add_field(name="`/gif [query]`", value="Get a random GIF", inline=False)
            embed_fun.add_field(name="`/chat-gpt [message]`", value="Chat with GPT", inline=False)
            embed_fun.add_field(name="`/image-gpt [message]`", value="Generation image with GPT", inline=False)
            embed_fun.set_image(url=banner)

            await interaction.response.edit_message(embed=embed_fun)

        if select.values[0] == "Moderation":
            # Embed moderation
            embed_mod = discord.Embed(
                title="<:mephisto:940249600969801748> **Mephisto Moderation Commands**",
                color=0x4a0000)
            embed_mod.add_field(name="`/clear [amount]`", value="Clear messages", inline=False)
            embed_mod.add_field(name="`/ban [user]`", value="Ban someone user", inline=False)
            embed_mod.add_field(name="`/kick [user]`", value="Kick someone user", inline=False)
            embed_mod.set_image(url=banner)

            await interaction.response.edit_message(embed=embed_mod)

        # if select.values[0] == "Other":
        #     # Embed music
        #     embed_other = discord.Embed(
        #         title="<:mephisto:940249600969801748> **Mephisto Other Commands**",
        #         description=f"You can use `!help` for music commands", 
        #         color=0x2D0000)
        #     embed_other.set_footer(text="If you have any questions, pls feel free to contact : Grumpy#9760")            
        #     embed_other.set_image(url=banner)

        #     await interaction.response.edit_message(embed=embed_other)


class Help(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(
        name="help", 
        description="Get the list of commands"
    )
    async def help(
        self, 
        ctx: discord.ApplicationContext
    ):
        """description="Get the list of commands"""
        banner = configs.BANNER_HELP_COMMANDS
        embed = discord.Embed(
            title="📑 HELP MENU",
            description=f"<a:pin:949334222760456202> **Important Info**\n[Invite Bot MEPHISTO#1211](https://discord.com/oauth2/authorize?client_id=907184657668386836&permissions=8&scope=bot%20applications.commands)\n[Donate](https://ko-fi.com/mephistogrumpy)",
            color=0xDF0000)
        embed.set_footer(text="Select Other Help Categories", icon_url=self.bot.user.avatar.url)
        embed.set_image(url=banner)
        
        dropdowns=DropDownMenu()

        process_embed = discord.Embed(
            title=f"<a:Three_Points_Animated:944865491921547264> MEPHISTO Processing...",
            color=0xDF0000)

        message = await ctx.respond(embed=process_embed)
        time.sleep(1)
        await ctx.interaction.edit_original_response(embed=embed, view=dropdowns)

    @slash_command(
        guild_ids=[
            "906963283989368862",
            "869835496187121724"
        ],
        name="rules", 
        description="Get the list of rules in this server"
    )
    async def rules(
        self, 
        ctx: discord.ApplicationContext
    ):
        """Get the list of rules in server"""
        owner = "https://cdn.discordapp.com/avatars/353899973252874260/ebc4f117db1269fac37f8ac6823baeb5.webp?size=256"
        rule_embed = discord.Embed(
            title="SERVER RULES <a:Emoji_Sparkles:918049225110065162>", 
            description=f"1) **Respect others**\n• Any bullying, threats, discrimination or anything of that nature isn’t tolerated. Lets keep this a positive discord for people to have fun and hang out.\n\n2) **No NSFW content**\n• Do not post NSFW content in any channel, if you do so you risk getting muted or banned depending on the severity.\n\n3) **Do not spam**\n• This includes rapid messages, spam private messages, mass reacting in chat channels and microphone abuse.\n\n4) **Discord Tos** \n• We are following Discord Tos, you can read them here \n[Discord's Terms of Service](https://discord.com/terms)\n\n5) **Please don't talk about religion or politics**\n•We will delete message, if you continue we would ban you", 
            color=0xff0000    
        )
        rule_embed.set_image(url="https://cdn.discordapp.com/attachments/908053630425366538/948470855208427550/banner_server_rules.gif")
        rule_embed.set_footer(text="If you have any questions, pls feel free to contact : Grumpy#9760", icon_url=owner)

        process_embed = discord.Embed(
            title=f"<a:Three_Points_Animated:944865491921547264> MEPHISTO Processing...",
            color=0xDF0000)
        
        message = await ctx.respond(embed=process_embed)
        time.sleep(1)
        await ctx.interaction.edit_original_response(embed=rule_embed)

def setup(bot: Bot):
    bot.add_cog(Help(bot))
