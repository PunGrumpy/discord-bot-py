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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# MONGODB
client = MongoClient(MONGO_URL)
db = client["automod"]
db_words = db["words"]
db_links = db["links"]
BAD_WORD = [word['badword'] for word in db_words.find()]
SPAM_LINK = [link['spamlink'] for link in db_links.find()]

def update_database():
    client = MongoClient(MONGO_URL)
    db = client["automod"]
    db_words = db["words"]
    db_links = db["links"]
    BAD_WORD = [word['badword'] for word in db_words.find()]
    SPAM_LINK = [link['spamlink'] for link in db_links.find()]

# CHANNEL
MOD_LOG_CHANNEL_NAME = "logs"

# DECORATION
BANNER_HELP_COMMANDS = "https://cdn.discordapp.com/attachments/908053630425366538/949497528531976192/help_commands.gif"
