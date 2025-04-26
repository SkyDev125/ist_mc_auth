import discord
from discord.ext import commands
from beartype import beartype
from src.errors.db import SearchError
from src.db.db import db
from src.server.requests import *
import src.constants as const


@beartype
def setup(bot: commands.Bot) -> None:
    @bot.tree.command(
        name="unlink",
        description="Unlink your Minecraft account from your Discord account",
    )
    async def unlink(interaction: discord.Interaction) -> None:
        """unlink MC - Discord"""

        # verify if this command is in a guild
        if interaction.guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
                delete_after=const.DEFAULT_MESSAGE_DELETE_DELAY,
            )
            return

        # check for player in database
        player = None
        try:
            player = db.search_discord_id(str(interaction.user.id))
        except SearchError as e:
            print(f"SearchError: {e.message}")
            await interaction.response.send_message(
                "You have not been Authenticated Yet. This command can only be ran by authenticated users.\n\nIf you think this was a mistake, please contact a staff member.",
                ephemeral=True,
                delete_after=const.DEFAULT_MESSAGE_DELETE_DELAY,
            )
            return

        if not player["minecraft_name"]:
            await interaction.response.send_message(
                "You have not linked your Minecraft account yet.\n\nIf you think this was a mistake, please contact a staff member.",
                ephemeral=True,
                delete_after=const.DEFAULT_MESSAGE_DELETE_DELAY,
            )
            return

        # remove the role from the user
        try:
            if isinstance(interaction.user, discord.Member):
                assert const.linked_player_role, "Linked Player role is None"
                await interaction.user.remove_roles(const.linked_player_role)
            else:
                print("Interaction user is not a member of the guild.")
        except Exception as e:
            print(f"Failed to remove role from user: {e}")
            await interaction.response.send_message(
                "Failed to remove role from user. Please contact a staff member.\n\nIf you think this was a mistake, please contact a staff member.",
                ephemeral=True,
                delete_after=const.DEFAULT_MESSAGE_DELETE_DELAY,
            )
            return

        # remove the player from the whitelist
        try:
            await remove_player_from_whitelist(player)
        except Exception as e:
            print(f"Failed to remove player from whitelist: {e}")
            await interaction.response.send_message(
                "Failed to remove you from the Minecraft server whitelist. Please contact a staff member.\n\nIf you think this was a mistake, please contact a staff member.",
                ephemeral=True,
                delete_after=const.DEFAULT_MESSAGE_DELETE_DELAY,
            )
            return

        # remove the minecraft name from the database
        player["minecraft_name"] = None
        db.update_player(player)

        await interaction.response.send_message(
            "Your Minecraft account has been unlinked from your Discord account! to link it again, please use the `/link` command.",
            ephemeral=True,
            delete_after=const.DEFAULT_MESSAGE_DELETE_DELAY,
        )

    _ = unlink  # Silence unaccessed function warning
