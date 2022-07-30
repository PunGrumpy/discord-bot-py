import discord
import discord.ext
import datetime
import requests
import random
import configs
import time
import aiohttp

from discord.ext.commands import Bot, Cog
from discord.commands import (
    slash_command,
    Option
)

class Accpet(discord.ui.View):
    def __init__(self, ctx):
        self.ctx = ctx
        super().__init__(timeout=10)
    
    async def on_timeout(self):
        if self.message:
            await self.message.edit_original_message(view=None)

    @discord.ui.button(label="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Accept⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", style=discord.ButtonStyle.green)
    async def accpet(self, button: discord.ui.Button, interaction: discord.Interaction):
        check_embed = discord.Embed(title=f"MEPHISTO : Check Your DM Message...", color=0xff0000)
        await interaction.response.send_message(embed=check_embed, ephemeral=True)
        self.value = True
        await self.message.edit_original_message(view=None)
        time.sleep(1)
        self.stop()

start_time = datetime.datetime.now()
def timedelta_str(dt):
    days = dt.days
    hours, r = divmod(dt.seconds, 3600)
    minutes, sec = divmod(r, 60)

    if minutes == 1 and sec == 1:
        return '{0} days, {1} hours, {2} minute and {3} second.'.format(days, hours, minutes, sec)
    elif minutes > 1 and sec == 1:
        return '{0} days, {1} hours, {2} minutes and {3} second.'.format(days, hours, minutes, sec)
    elif minutes == 1 and sec > 1:
        return '{0} days, {1} hours, {2} minute and {3} seconds.'.format(days, hours, minutes, sec)
    else:
        return '{0} days, {1} hours, {2} minutes and {3} seconds.'.format(days, hours, minutes, sec)

class General(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Ping
    @slash_command(
        name="ping", 
        description="Return websocket ping"
    )
    async def ping(
        self, 
        ctx: discord.ApplicationContext
    ):
        """Return websocket ping"""
        user = ctx.author
        rand = random.randint(0x111, 0xFF0000)
        embed = discord.Embed(
            title="**PONG**",
            description=f"<a:Angryping:944880187886174208> **Latency** : `{round(self.bot.latency * 1000)} ms`",
            color=rand)
        embed.timestamp = datetime.datetime.utcnow()
        wait_embed = discord.Embed(title=f"<a:Three_Points_Animated:944865491921547264> Hang on a moment...",
                                   color=rand)
        message = await ctx.respond(embed=wait_embed)
        time.sleep(1)
        await ctx.interaction.edit_original_message(embed=embed)

    # Invite
    @slash_command(
        name="invite", 
        description="Invite bot to your server"
    )
    async def invite(
        self, 
        ctx: discord.ApplicationContext
    ):
        """Invite bot to your server"""
        embed = discord.Embed(
            title="Invite Mephisto",
            description=
            "**Invite Me To Your Server**\nInvite Link : [Link](https://discord.com/oauth2/authorize?client_id=907184657668386836&permissions=8&scope=bot%20applications.commands)\nWebsite Link : [Link](https://mephisto-website-bot.web.app/)",
            color=0xff0000)
        embed.set_image(
            url=
            "https://cdn.discordapp.com/attachments/908053630425366538/935793328954421258/Mephisto_Animation.gif"
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Requested by - {ctx.author}',
                         icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)

    # Weather
    @slash_command(
        name="weather", 
        description="Get the weather of the city you want to know"
    )
    async def weather(
        self, 
        ctx: discord.ApplicationContext, 
        city: Option(str, "Specify the city you want to know")
    ):
        """Get the weather of the city you want to know"""
        api_key = configs.WEATHER_API_KEY
        base_url = "http://api.openweathermap.org/data/2.5/weather?"

        city_name = city
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()

        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_temperature_celsiuis = str(
                round(current_temperature - 273.15))
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            embed = discord.Embed(title=f"Weather in {city_name}",
                                  color=ctx.guild.me.top_role.color)
            embed.timestamp = datetime.datetime.utcnow()
            embed.add_field(name="Descripition",
                            value=f"**{weather_description}**",
                            inline=False)
            embed.add_field(name="Temperature(C)",
                            value=f"**{current_temperature_celsiuis}°C**",
                            inline=False)
            embed.add_field(name="Humidity(%)",
                            value=f"**{current_humidity}%**",
                            inline=False)
            embed.add_field(name="Atmospheric Pressure(hPa)",
                            value=f"**{current_pressure}hPa**",
                            inline=False)
            embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            find_embed = discord.Embed(title=f"<a:Three_Points_Animated:944865491921547264> MEPHISTO Finding...",
                                       color=ctx.guild.me.top_role.color)
            message = await ctx.respond(embed=find_embed)
            time.sleep(1)
            await ctx.interaction.edit_original_message(embed=embed)

        else:
            embed = discord.Embed(title=f"ERROR",
                                  color=ctx.guild.me.top_role.color)
            embed.timestamp = datetime.datetime.utcnow()
            embed.add_field(name="**City Not Found**",
                            value=f"{city_name}",
                            inline=False)
            embed.add_field(name="**Example city**",
                            value=f"Bangkok\nEngland\netc.",
                            inline=False)
            embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            find_embed = discord.Embed(title=f"<a:Three_Points_Animated:944865491921547264> MEPHISTO Finding...",
                                       color=ctx.guild.me.top_role.color)
            message = await ctx.respond(embed=find_embed)
            time.sleep(1)
            await ctx.interaction.edit_original_message(embed=embed)

    # Donut ASCII
    @slash_command(
        name="donut", 
        description="Send ASCII art donut spinning"
    )
    async def donut(
        self, 
        ctx
    ):
        """Send ASCII art donut spinning"""
        embed = discord.Embed(title="ASCII DONUT" ,color=0xff0000)
        embed.set_image(
            url=
            "https://cdn.discordapp.com/attachments/908053630425366538/936518564930793472/donut_animation.gif"
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'If you want file donut_ascii.py, you click accept',
                         icon_url=ctx.author.avatar.url)
        
        view = Accpet(ctx)
        view.message = await ctx.respond(embed=embed, view=view)
        await view.wait()
        if view.value is None:
            return
        elif view.value:
            await ctx.author.send(file=discord.File('donut_ascii.py'))
            return

    # Uptime
    @slash_command(
        name="uptime", 
        description="Time during which a machine, especially a computer, is in operation"
    )
    async def uptime(
        self, 
        ctx: discord.ApplicationContext
    ):
        """Time during which a machine, especially a computer, is in operation"""
        global start_time
        embed = discord.Embed(
            title="**Uptime**",
            description=f"{timedelta_str(datetime.datetime.now()-start_time)}",
            color=discord.Color.green())
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Requested by - {ctx.author}',
                     icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)

    # Bitcoin price
    @slash_command(description="Get the current price of bitcoin" )
    async def bitcoin(self, ctx: discord.ApplicationContext) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.coindesk.com/v1/bpi/currentprice/BTC.json") as request:
                if request.status == 200:
                    data = await request.json(
                        content_type="application/javascript")  # For some reason the returned content is of type JavaScript
                    embed = discord.Embed(
                        title="Bitcoin price",
                        description=f"The current price is **{data['bpi']['USD']['rate']}** <a:bitcoin_8bit:948230457126957146>",
                        color=0xF7931A
                    )
                    embed.set_footer(text=f'Requested by - {ctx.author}', icon_url=ctx.author.avatar.url)
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                find_embed = discord.Embed(title=f"<a:Three_Points_Animated:944865491921547264> MEPHISTO Finding...",
                                       color=0xF7931A)
                message = await ctx.respond(embed=find_embed)
                time.sleep(1)
                await ctx.interaction.edit_original_message(embed=embed)

   
def setup(bot: Bot):
    bot.add_cog(General(bot))
