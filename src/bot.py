import discord
from discord.ext import commands

from dotenv import load_dotenv
from os import getenv

from src.commands import load_commands
from src.events import load_events

# Load environment variables
load_dotenv()
token = getenv("BOT_TOKEN")
if token is None:
    raise ValueError("BOT_TOKEN environment variable is not set.")

# Create bot instance
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="?", intents=intents)

# Load commands and events
load_commands(bot)
load_events(bot)

# Run bot
bot.run(token)
