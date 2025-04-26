import typing
import discord
from discord import ui

import src.constants as const
from src.errors.db import SearchError
from src.server.requests import *
from src.db.db import db

class MinecraftAccountLinking(ui.Modal, title="Link Minecraft Account"):
    # Define the text input field
    # The attribute name (`mc_username`) is how you'll access the value later
    mc_username: ui.TextInput[typing.Self] = ui.TextInput(
        label="Minecraft Username",
        placeholder="Steve",
        style=discord.TextStyle.short,
        required=True,
        max_length=30,
        min_length=3,
    )

    # This method is called when the user clicks the "Submit" button
    async def on_submit(self, interaction: discord.Interaction):
        # Get the value entered by the user from the TextInput attribute
        username = self.mc_username.value
        discord_id = interaction.user.id

        # Check if the username exists
        if not await fetch_uuid_async(username):
            await interaction.response.send_message(
                "That username does not exist. Please try again.\n\nIf you think this was a mistake, please contact a staff member.",
                ephemeral=True,
                delete_after=const.DEFAULT_MESSAGE_DELETE_DELAY,
            )
            return

        # Check if the player exists in the database
        player = None
        try:
            player = db.search_discord_id(str(discord_id))
        except SearchError as e:
            print(f"SearchError: {e.message}")
            await interaction.response.send_message(
                "You have not been Authenticated Yet. Please try again.\n\nIf you think this was a mistake, please contact a staff member.",
                ephemeral=True,
                delete_after=const.DEFAULT_MESSAGE_DELETE_DELAY,
            )
            return

        # Check if the username is already linked to another user
        try:
            result = db.search_minecraft_name(username)
            if result and result["discord_id"] != str(discord_id):
                await interaction.response.send_message(
                    "That username is already linked to another account. Please try again.\n\nIf you think this was a mistake, please contact a staff member.",
                    ephemeral=True,
                    delete_after=const.DEFAULT_MESSAGE_DELETE_DELAY,
                )
                return
        except SearchError as e:
            pass  # No player found with that username, so we can proceed

        # Update the player's Minecraft username in the database
        player["minecraft_name"] = username
        db.update_player(player)

        # Give the user the linked player role
        try:
            if isinstance(interaction.user, discord.Member):
                assert const.linked_player_role, "Linked Player role is None"
                await interaction.user.add_roles(const.linked_player_role)
            else:
                print("Interaction user is not a member of the guild.")
        except Exception as e:
            print(f"Failed to add role to user: {e}")
            await interaction.response.send_message(
                "Failed to add role to user. Please contact a staff member.\n\nIf you think this was a mistake, please contact a staff member.",
                ephemeral=True,
                delete_after=const.DEFAULT_MESSAGE_DELETE_DELAY,
            )

        # Whitelist the user on the Minecraft server
        try:
            await add_player_to_whitelist(player)
        except Exception as e:
            print(f"Failed to whitelist player: {e}")
            await interaction.response.send_message(
                "Failed to whitelist you on the Minecraft server. Please contact a staff member.\n\nIf you think this was a mistake, please contact a staff member.",
                ephemeral=True,
                delete_after=const.DEFAULT_MESSAGE_DELETE_DELAY,
            )
            return

        # Send a confirmation message back to the user (ephemeral is usually best)
        await interaction.response.send_message(
            f"Okay, I've recorded your Minecraft username as: `{username}` and you've been whitlisted on the minecraft server! Thanks!",
            ephemeral=True,
            delete_after=const.DEFAULT_MESSAGE_DELETE_DELAY,
        )

    # Optional: Handle errors if submission fails for some reason
    async def on_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        print(f"Error in MinecraftUsernameModal: {error}")  # Log the error
        # Notify the user something went wrong
        try:
            # Check if response already sent, use followup if needed
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "Oops! Something went wrong submitting your username.",
                    ephemeral=True,
                )
            else:
                await interaction.followup.send(
                    "Oops! Something went wrong submitting your username.",
                    ephemeral=True,
                )
        except Exception as followup_error:
            print(f"Failed to send error message to user: {followup_error}")