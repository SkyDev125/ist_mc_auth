import discord
from discord.ext import commands
from beartype import beartype
from src.modals.minecraft import MinecraftUsernameModal
import src.constants as const


@beartype
def setup(bot: commands.Bot) -> None:
    @bot.tree.command(
        name="link",
        description="Get your minecraft account linked to your discord account",
    )
    async def link(interaction: discord.Interaction) -> None:
        """Link MC - Discord"""

        # verify if this command is in a guild
        if interaction.guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
                delete_after=const.DEFAULT_MESSAGE_DELETE_DELAY,
            )
            return

        # send modal requesting user's minecraft name
        modal = MinecraftUsernameModal()
        await interaction.response.send_modal(modal)

    _ = link  # Silence unaccessed function warning
