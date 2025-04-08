from discord.ext.commands import Bot
import discord
from beartype import beartype

from os import getenv


@beartype
def setup(bot: Bot) -> None:
    @bot.event
    async def on_ready() -> None:
        # Print bot information
        if bot.user is not None:
            print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
        else:
            print("❌ Bot user is None. Login might have failed.")
        print("------")

        # Sync slash commands to guild
        test_guild = getenv("GUILD_ID")
        if test_guild is None:
            print(
                "⚠️ GUILD_ID environment variable is not set. Skipping slash command sync to guild."
            )
            return
        test_guild = discord.Object(id=int(test_guild))
        try:
            bot.tree.copy_global_to(guild=test_guild)
            synced = await bot.tree.sync(guild=test_guild)
            print(f"✅ Synced {len(synced)} slash commands to guild {test_guild.id}.")
        except Exception as e:
            print(f"⚠️ Failed to sync slash commands to guild {test_guild.id}: {e}")
        print("------")

    _ = on_ready  # Silence unaccessed function warning
