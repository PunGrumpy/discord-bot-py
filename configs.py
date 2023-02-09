import os
from dotenv import load_dotenv
from pymongo import MongoClient

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
client = MongoClient(MONGO_URL)
db = client["discord"]
db_word = db["word"]
db_link = db["link"]

for words in db_word.find():
    BAD_WORD = words["word"]

for links in db_link.find():
    SPAM_LINK = links["link"]

# DECORATION
BANNER_HELP_COMMANDS = "https://cdn.discordapp.com/attachments/908053630425366538/949497528531976192/help_commands.gif"
