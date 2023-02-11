import discord
import discord.ext
import datetime
import time
import platform
import os, psutil
import cpuinfo

from io import BytesIO
from PIL import Image, ImageChops, ImageDraw, ImageFont

from discord.ext.commands import Bot, Cog
from discord.ui import View, Button
from discord.commands import (
    slash_command,
    Option
)


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

def circle(pfp,size = (215,215)):
    
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp


class Infomation(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # User info
    @slash_command(
        name="user-info", 
        description="Get a profile someone"
    )
    async def userinfo(
        self, 
        ctx, 
        user : Option(discord.User, "specific user you want to know")
    ):
      """Get a profile someone"""
      name, Id, status, top_role, bot = str(user), str(user.id), str(user.status), str(user.top_role), str(user.bot)

      today = discord.utils.utcnow()

      created_at = user.created_at
      joined_at = user.joined_at

      delta_created = f"{(today - created_at).days} days"
      delta_joined = f"{(today - joined_at).days} days"

      base = Image.open("base.png").convert("RGBA")

      pfp = user.avatar.with_format('png').with_size(256)
      data = BytesIO(await pfp.read())
      pfp = Image.open(data).convert("RGBA")

      name = f"{name[:16]}.." if len(name)>16 else name

      draw = ImageDraw.Draw(base)
      pfp = circle(pfp,(215,215))
      font = ImageFont.truetype("Nunito-Bold.ttf", 38)
      subfont = ImageFont.truetype("Nunito-Regular.ttf", 25)

      draw.text((280,240), name,font = font)

      draw.text((65,490), Id,font = subfont)
      draw.text((405,490), status,font = subfont)

      draw.text((65,635), bot,font = subfont)
      draw.text((405,635), top_role,font = subfont)
      
      draw.text((65,765), created_at.strftime("%a %d %b %y"),font = subfont)
      draw.text((65,800), delta_created,font = subfont)
      draw.text((405,765), joined_at.strftime("%a %d %b %y"),font = subfont)
      draw.text((405,800), delta_joined,font = subfont)
      base.paste(pfp,(56,158),pfp)

      base.paste(base,(0,0),base)

      with BytesIO() as a:
        base.save(a,"PNG")
        a.seek(0)
        if not os.path.exists("./assets/user"):
            os.mkdir("./assets/user")
        wait_embed = discord.Embed(title=f"<a:Three_Points_Animated:944865491921547264> User Information", description=f"Please wait, we are generating your profile", color=discord.Color.green())
        await ctx.respond(embed=wait_embed, delete_after=5)
        await ctx.send(file = discord.File(a, "user.png"))

    # Bot info
    @slash_command(
        name="bot-info", 
        description="Get information about Mephisto bot"
    )
    async def botinfo(
        self, 
        ctx: discord.ApplicationContext
    ):
        """Get information about Mephisto bot"""
        CPUBRAND = cpuinfo.get_cpu_info()['brand_raw']
        vcpu = psutil.cpu_percent()
        process = psutil.Process(os.getpid())
        memory_total = (psutil.virtual_memory().total / 1024 / 1024 / 1024)
        memory_total_str = "{:.2f}".format(memory_total)
        memory_usage = (process.memory_info().rss / 1024 / 1024 / 1024)
        memory_usage_str = "{:.2f}".format(memory_usage)
        Owner = await self.bot.fetch_user(353899973252874260)
        embed = discord.Embed(title=f"Mephisto Information", description=f"`Owner:` {Owner.mention}\n`Python Version:` {platform.python_version()}\n`Discord version:` {discord.__version__}\n```OS : {platform.system()} {platform.architecture()[0]}\nCPU : {CPUBRAND}\nCPU USAGE : {vcpu} %\nRAM : {memory_usage_str} / {memory_total_str} GB```",
                              color=discord.Color.red())
        embed.set_footer(text=f'{self.bot.user} | ⏱️ Uptime : {timedelta_str(datetime.datetime.now()-start_time)}',
                         icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(
            url=
            "https://cdn.discordapp.com/attachments/908053630425366538/946441076569440276/mephisto-mephisto-clap.gif"
        )
        find_embed = discord.Embed(
            title=f"<a:Three_Points_Animated:944865491921547264> MEPHISTO Finding...",
            color=0xFF0000)
        website = Button(label="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Website⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", url="https://mephisto-website-bot.web.app/", style=discord.ButtonStyle.url)
        view = View()
        view.add_item(website)
        view.message = await ctx.respond(embed=find_embed)
        time.sleep(1)
        await ctx.interaction.edit_original_response(embed=embed, view=view)

    
    # Server info
    @slash_command(
        name="server-info", 
        description="Get information about this Server"
    )
    async def serverinfo(
        self, 
        ctx: discord.ApplicationContext
    ):
        """Server info"""
        role_count = len(ctx.guild.roles)
        list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]
        owner = str(ctx.guild.owner)

        embed = discord.Embed(color=ctx.author.color)
        embed.timestamp = datetime.datetime.utcnow()
        embed.add_field(name='Name', value=f"{ctx.guild.name}", inline=False)
        embed.add_field(name='Owner', value=f"{owner}", inline=False)
        embed.add_field(name='Verification Level',
                        value=str(ctx.guild.verification_level),
                        inline=False)
        embed.add_field(name='Highest role',
                        value=ctx.guild.roles[-1].mention,
                        inline=False)
        embed.add_field(name='Number of roles',
                        value=str(role_count),
                        inline=False)
        embed.add_field(name='Number Of Members',
                        value=ctx.guild.member_count,
                        inline=False)
        embed.add_field(name='Bots:', value=(', '.join(list_of_bots)))
        embed.add_field(name='Created At',
                        value=ctx.guild.created_at.__format__(
                            '%A, %d %B %Y (%H:%M:%S %ZGMT)'),
                        inline=False)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_footer(text=f'Requested by - {ctx.author}',
                         icon_url=ctx.author.avatar.url)

        think_embed = discord.Embed(
            title=f"<a:Three_Points_Animated:944865491921547264> MEPHISTO Finding Information About Server...",
            color=ctx.guild.owner.top_role.color)
        message = await ctx.respond(embed=think_embed)
        time.sleep(1)
        await ctx.interaction.edit_original_response(embed=embed)
      


def setup(bot: Bot):
    bot.add_cog(Infomation(bot))
