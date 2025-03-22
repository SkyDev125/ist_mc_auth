from discord.ext.commands import Bot
from discord.ext.commands.context import Context


def setup(bot: Bot) -> None:
    @bot.command()
    async def ping(ctx: Context[Bot]) -> None:
        await ctx.send("🏓 Pong from Skythentic!")

    _ = ping  # Silence unaccessed function warning
