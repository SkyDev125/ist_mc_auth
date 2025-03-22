import discord
from discord.ext import commands


def setup(bot: commands.Bot) -> None:
    @bot.tree.command(name="ping", description="Ping command")
    async def ping(interaction: discord.Interaction) -> None:
        await interaction.response.send_message("🏓 Pong from Skythentic!")

    _ = ping  # Silence unaccessed function warning
