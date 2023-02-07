from os import environ

# SECRET
DISCORD_TOKEN = environ.get("DISCORD_TOKEN")
GIPHY_API_KEY = environ.get("GIPHY_API_KEY")
MONGO_URL = environ.get("MONGO_URL")
GITHUB_TOKEN = environ.get("GITHUB_TOKEN")
WEATHER_API_KEY = environ.get("WEATHER_API_KEY")
OWNER_ID = environ.get("OWNER_ID")

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
