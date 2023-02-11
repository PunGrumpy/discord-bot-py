import discord
import discord.ext
import requests
import configs
import random
import json
import time
import openai

from discord.ext.commands import Bot, Cog
from discord.commands import (
    slash_command,
    Option
)

openai.api_key = configs.OPENAI_API_KEY

class NitroAccept(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Accept⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", style=discord.ButtonStyle.green)
    async def nitro(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("https://images-ext-1.discordapp.net/external/AoV9l5YhsWBj92gcKGkzyJAAXoYpGiN6BdtfzM-00SU/https/i.imgur.com/NQinKJB.mp4", ephemeral=True)
        self.value = True
        self.stop()

class NitroDisable(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Accept⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", style=discord.ButtonStyle.secondary, disabled=True)
    async def nitro(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = True
        self.stop()

class Fun(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Joke
    @slash_command(
        name="joke", 
        description="Get a random joke"
    )
    async def joke(
        self, 
        ctx: discord.ApplicationContext
    ):
        """Get a random joke"""
        rand = random.randint(0x111, 0xFF0000)
        response = requests.get(
            "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,racist&type=single"
        )
        json_data = json.loads(response.text)
        joke = json_data["joke"]
        embed = discord.Embed(title="<a:lol_1:944867138932449322> JOKE",
                              description=f'{joke}',
                              color=rand)
        embed.set_footer(text=f'Requested by - {ctx.author}',
                         icon_url=ctx.author.avatar.url)
        random_embed = discord.Embed(title=f"<a:Three_Points_Animated:944865491921547264> MEPHISTO Randomizing A Joke...",
                                     color=rand)
        message = await ctx.respond(embed=random_embed)
        time.sleep(1)
        await ctx.interaction.edit_original_response(embed=embed)

    # Meme
    @slash_command(
        name="meme", 
        description='Get a random meme'
    )
    async def meme(
        self, 
        ctx: discord.ApplicationContext
    ):
        """Get a random meme"""
        rand = random.randint(0x000, 0xFF0000)
        content = requests.get("https://meme-api.herokuapp.com/gimme").text
        data = json.loads(content)
        meme = discord.Embed(title="<a:PepeLmfaoooo:944951463640186950> MEME",
                             color=rand).set_image(url=f"{data['url']}")
        meme.set_footer(text=f'Requested by - {ctx.author}',
                        icon_url=ctx.author.avatar.url)
        random_embed = discord.Embed(title=f"<a:Three_Points_Animated:944865491921547264> MEPHISTO Randomizing A Meme...",
                                     color=rand)
        message = await ctx.respond(embed=random_embed)
        time.sleep(1)
        await ctx.interaction.edit_original_response(embed=meme)

    # 8 ball
    @slash_command(
        name="8ball", 
        description='Let the 8 Ball Predict!'
    )
    async def eightball(
        self, 
        ctx: discord.ApplicationContext, 
        question: Option(str, "Enter the question")
    ):
        """Let the 8 Ball Predict!"""
        responses = ['As I see it, yes.',
             'Yes.',
             'Positive',
             'From my point of view, yes',
             'Convinced.',
             'Most Likely.',
             'Chances High',
             'No.',
             'Negative.',
             'Not Convinced.',
             'Perhaps.',
             'Not Sure',
             'Maybe',
             'I cannot predict now.',
             'Im to lazy to predict.',
             'I am tired. *proceeds with sleeping*']
        response = random.choice(responses)
        rand = random.randint(0x000, 0xFF0000)
        embed=discord.Embed(title="<a:lol_2:944951819111632947> The Magic 8 Ball has Spoken!", color=rand)
        embed.add_field(name='Question: ', value=f'{question}', inline=True)
        embed.add_field(name='Answer: ', value=f'{response}', inline=False)
        await ctx.respond(embed=embed)

    # GIPHY
    @slash_command(
        name="gif", 
        description="Get GIF that you want"
    )
    async def gif(
        self, 
        ctx: discord.ApplicationContext, 
        search: Option(str, "Specific the GIF that you want")
    ):
        """Get GIF that you want"""
        giphy_api = configs.GIPHY_API_KEY
        
        rand = random.randint(0x000, 0xFF0000)
        embed = discord.Embed(color=rand)
        embed.set_footer(text=f'Requested by - {ctx.author}', icon_url=ctx.author.avatar.url)
        find_embed = discord.Embed(title=f"<a:Three_Points_Animated:944865491921547264> MEPHISTO Finding A GIF...", color=rand)
        
        response = requests.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=' + giphy_api + '&limit=10')
        json_data = json.loads(response.text)
        gif_choice = random.randint(0, 9)
        gif = json_data['data'][gif_choice]['images']['original']['url']
        embed.set_author(name=f"🎉 {search}")
        embed.set_image(url=gif)
        message = await ctx.respond(embed=find_embed)
        time.sleep(1)
        await ctx.interaction.edit_original_response(embed=embed)

    # Fake nitro
    @slash_command(
        name='nitro', 
        description="Send a totally not a scamming nitro message that totally would not hack a Discord Account!",
    )
    async def nitro(
        self, 
        ctx: discord.ApplicationContext
    ):
        button_before = NitroAccept()
        button_after = NitroDisable()
        embed_before = discord.Embed(
            title="You've been gifted a subscription!",
            description="You've been gifted a **1 Month Nitro Subscription!**", 
            color = 0x2C2F33
        )
        embed_before.set_thumbnail(url="https://images-ext-2.discordapp.net/external/sVYV81qlzJcVdaE0xE7wdxeNkS2PzfKCpQvB2sqNG7k/https/i.imgur.com/w9aiD6F.png")

        embed_after = discord.Embed(
            title="You've been gifted a subscription!",
            description="Uh oh, looks like someone already claimed this gift.", 
            color = 0x2C2F33
        )
        embed_after.set_thumbnail(url="https://images-ext-2.discordapp.net/external/sVYV81qlzJcVdaE0xE7wdxeNkS2PzfKCpQvB2sqNG7k/https/i.imgur.com/w9aiD6F.png")
        message = await ctx.respond(embed=embed_before, view=button_before)
        await button_before.wait()
        await ctx.interaction.edit_original_response(embed=embed_after, view=button_after)
        await ctx.respond(f"<a:jokerlaugh:949318686156681267>")

    # Chat GPT
    @slash_command(
        name="chat-gpt",
        description="Chat with GPT",
        message=Option(
            str,
            "Enter the message that you want to chat with GPT",
            required=True
        )
    )
    async def chatgpt(
        self, 
        ctx: discord.ApplicationContext, 
        message
    ):
        """Chat with GPT"""
        rand = random.randint(0x111, 0xFF0000)
        process_embed = discord.Embed(title=f"<a:Three_Points_Animated:944865491921547264> MEPHISTO Processing with Chat GPT...", color=rand)
        waiting = await ctx.respond(embed=process_embed)

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=message,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            best_of=1,
        )
        embed = discord.Embed(title=f"<a:lol_2:944951819111632947> Chat GPT", description=f"```{response['choices'][0]['text']}```", color=rand)
        await ctx.interaction.edit_original_response(embed=embed)

    # Generate Image with GPT
    @slash_command(
        name="image-gpt",
        description="Generate an image with GPT",
        message=Option(
            str,
            "Enter the message that you want to generate an image with GPT",
            required=True
        )
    )
    async def imagegpt(
        self, 
        ctx: discord.ApplicationContext, 
        message
    ):
        """Generate an image with GPT"""
        rand = random.randint(0x111, 0xFF0000)
        process_embed = discord.Embed(title=f"<a:Three_Points_Animated:944865491921547264> MEPHISTO Processing with Draw GPT...", color=rand)
        waiting = await ctx.respond(embed=process_embed)

        response = openai.Image.create(
            prompt=message,
            n=1,
            size="1024x1024"
        )
        image = response['data'][0]['url']
        embed = discord.Embed(title=f"<a:lol_2:944951819111632947> Generate Image", color=rand)
        embed.set_image(url=image)
        await ctx.interaction.edit_original_response(embed=embed)

def setup(bot: Bot):
    bot.add_cog(Fun(bot))
