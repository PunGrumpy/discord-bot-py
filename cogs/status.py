import discord
import requests
import dateutil.parser
import os
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw

from discord.ext.commands import Bot, Cog
from discord.ext import commands
from discord.commands import (
    slash_command,
    Option
)


class Spotify(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(
        name="spotify-status", 
        description="Shows the song the user is listening to"
    )
    async def spotifystatus(
        self, 
        ctx: discord.ApplicationContext, 
        user: Option(discord.User, "Specific user you want to know")
    ):
        """Shows the song the user is listening to"""
        if not user:
            user = ctx.author

        spotify_result = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)

        if spotify_result is None:
            await ctx.respond(f"{user.name} is not listening to Spotify. <a:alert:944877266402435092>")

        # Images
        track_background_image = Image.open('./assets/images/spotify-status/spotify_template.png')
        album_image = Image.open(requests.get(spotify_result.album_cover_url, stream=True).raw).convert('RGBA')

        # Fonts
        title_font = ImageFont.truetype('./assets/fonts/theboldfont.ttf', 16)
        artist_font = ImageFont.truetype('./assets/fonts/theboldfont.ttf', 14)
        album_font = ImageFont.truetype('./assets/fonts/theboldfont.ttf', 14)
        start_duration_font = ImageFont.truetype('./assets/fonts/theboldfont.ttf', 12)
        end_duration_font = ImageFont.truetype('./assets/fonts/theboldfont.ttf', 12)

        # Positions
        title_text_position = 150, 30
        artist_text_position = 150, 60
        album_text_position = 150, 80
        start_duration_text_position = 150, 122
        end_duration_text_position = 515, 122

        # Draws
        draw_on_image = ImageDraw.Draw(track_background_image)
        draw_on_image.text(title_text_position, spotify_result.title, 'white', font=title_font)
        draw_on_image.text(artist_text_position, f'by {spotify_result.artist}', 'white', font=artist_font)
        draw_on_image.text(album_text_position, spotify_result.album, 'white', font=album_font)
        draw_on_image.text(start_duration_text_position, '0:00', 'white', font=start_duration_font)
        draw_on_image.text(end_duration_text_position,
                           f"{dateutil.parser.parse(str(spotify_result.duration)).strftime('%M:%S')}",
                           'white', font=end_duration_font)

        # Background colour
        album_color = album_image.getpixel((250, 100))
        background_image_color = Image.new('RGBA', track_background_image.size, album_color)
        background_image_color.paste(track_background_image, (0, 0), track_background_image)

        # Resize
        album_image_resize = album_image.resize((140, 160))
        background_image_color.paste(album_image_resize, (0, 0), album_image_resize)

        # Check spotify-status folder
        if not os.path.exists('./assets/images/spotify-status'):
            os.makedirs('./assets/images/spotify-status')

        # Save image
        background_image_color.convert('RGB').save('./assets/images/spotify-status/spotify.jpg', 'JPEG')

        await ctx.respond(file=discord.File('./assets/images/spotify-status/spotify.jpg'))


def setup(bot):
    bot.add_cog(Spotify(bot))