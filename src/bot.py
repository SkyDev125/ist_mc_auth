import discord
from discord.ext import commands

import asyncio

# Import custom modules
from dotenv import load_dotenv
from os import getenv

from src.commands import load_commands
from src.events import load_events
from src.server import web_server

# Load environment variables
load_dotenv()
token = getenv("BOT_TOKEN")


async def main():
    if token is None:
        raise ValueError("BOT_TOKEN environment variable is not set.")

    # Create bot instance
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="?", intents=intents)

    # Load commands and events
    load_commands(bot)
    load_events(bot)

    # Run bot
    try:
        await web_server.start_server(bot)
        await bot.start(token)
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await bot.close()
        await web_server.stop_server()


# Run the main async function
try:
    asyncio.run(main())
except KeyboardInterrupt:
    # Catch the KeyboardInterrupt raised by asyncio.run()
    print("\nProgram finished gracefull exit.")
