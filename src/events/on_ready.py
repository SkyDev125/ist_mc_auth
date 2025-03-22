from discord.ext.commands import Bot


def setup(bot: Bot) -> None:
    @bot.event
    async def on_ready() -> None:
        if bot.user is not None:
            print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
        else:
            print("❌ Bot user is None. Login might have failed.")
        print("------")

    _ = on_ready  # Silence unaccessed function warning
