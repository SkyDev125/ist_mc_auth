import discord
from discord.ext import commands
from beartype import beartype
from src.server import web_server
from src.db.db import db
from src.constants import *


@beartype
def setup(bot: commands.Bot) -> None:
    @bot.tree.command(name="auth", description="Authenticate to get access (Fenix)")
    async def auth(interaction: discord.Interaction) -> None:
        """Authenticate the user with the web server."""

        # if the user already exists in the database
        try:
            db.search_discord_id(str(interaction.user.id))
            await interaction.response.send_message(
                "You are already authenticated. If you think this is a mistake, please contact the server administrators.",
                ephemeral=True,
                delete_after=DEFAULT_MESSAGE_DELETE_DELAY,
            )

        # if the user doesn't exist in the database
        except Exception:
            await interaction.response.send_message(
                "Authentication process started. Please check your DMs for further instructions.",
                ephemeral=True,
                delete_after=DEFAULT_MESSAGE_DELETE_DELAY,
            )
            url = await web_server.create_auth_url(interaction)
            await interaction.user.send(
                "To authenticate, please click the link below:\n\n"
                f"{url}\n\n"
                "If you encounter any issues, please contact the server administrators.",
                delete_after=DEFAULT_MESSAGE_DELETE_DELAY,
            )

    _ = auth  # Silence unaccessed function warning
