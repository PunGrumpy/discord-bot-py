import os
from dotenv import load_dotenv

load_dotenv()

# SECRET
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")
MONGO_URL = os.getenv("MONGO_URL")
GITHUB_TOKEN =  os.getenv("GITHUB_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
OWNER_ID = os.getenv("OWNER_ID")

# CHANNEL
MOD_LOG_CHANNEL_NAME = "logs"

# AUTOMOD
BAD_WORD = [
            'dick', 'pussy', 'bitch', 'cock', 'fuck', 'FUCK', 'f u c k',
            'F U C K', 'sex', 'shit', 's h i t', 'wtf', 'WTF', 'w t f',
            'W T F', 'พ่อมึงตาย', 'แม่มึงตาย', 'ควย', 'ค ว ย', 'ครวย',
            'ค ร ว ย', 'หี'
        ]
        
SPAM_LINK = [
            'Get Discord Nitro for Free from Steam Store',
            'https://dlsccord-app.com/welcome',
            'https://streamconmunitly.ru/nitro/x27t6cPt1cwOPf36', 
            'free nitro'
        ]

# DECORATION
BANNER_HELP_COMMANDS = "https://cdn.discordapp.com/attachments/908053630425366538/949497528531976192/help_commands.gif"
