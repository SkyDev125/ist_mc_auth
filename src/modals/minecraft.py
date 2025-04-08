import typing
import discord
from discord import ui  # Import the ui module

# --- The Modal Class Definition ---


class MinecraftUsernameModal(ui.Modal, title="Link Minecraft Account"):
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
        discord_user_id = interaction.user.id

        # --- TODO: Process the received username ---
        # Examples:
        # 1. Print it to console
        print(
            f"Received Minecraft Username from Discord User {discord_user_id}: {username}"
        )
        # 2. Store it in your database/json file linked to the discord_user_id
        #    (You would add your data storage logic here)
        # 3. Potentially validate the username format or check against Mojang API (more complex)

        # Send a confirmation message back to the user (ephemeral is usually best)
        await interaction.response.send_message(
            f"Okay, I've recorded your Minecraft username as: `{username}`. Thanks!",
            ephemeral=True,
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
