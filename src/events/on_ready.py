from discord.ext.commands import Bot
from beartype import beartype

import src.constants as const


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

        if not const.GUILD_ID:
            print(
                "⚠️ GUILD_ID environment variable is not set. Skipping slash command sync to guild."
            )
            return

        # Check if the guild is valid
        const.guild = bot.get_guild(int(const.GUILD_ID))
        if not const.guild:
            print(f"⚠️ Guild with ID {const.GUILD_ID} not found.")
            return

        # Sync slash commands to the guild
        try:
            bot.tree.copy_global_to(guild=const.guild)
            synced = await bot.tree.sync(guild=const.guild)
            print(f"✅ Synced {len(synced)} slash commands to guild {const.guild.id}.")
        except Exception as e:
            print(f"⚠️ Failed to sync slash commands to guild {const.guild.id}: {e}")
            return
        print("------")

        const.ist_player_role = const.guild.get_role(const.IST_PLAYER_ROLE_ID)
        const.guest_player_role = const.guild.get_role(const.GUEST_PLAYER_ROLE_ID)
        const.linked_player_role = const.guild.get_role(const.LINKED_PLAYER_ROLE_ID)

        if not const.ist_player_role:
            print("⚠️ IST_PLAYER_ROLE_ID role not found.")

        if not const.guest_player_role:
            print("⚠️ GUEST_PLAYER_ROLE_ID role not found.")

        if not const.linked_player_role:
            print("⚠️ LINKED_PLAYER_ROLE_ID role not found.")

        print(
            f"✅ Roles verified in guild '{const.guild}': "
            f"ist_player_role: '{const.ist_player_role}', "
            f"guest_player_role: '{const.guest_player_role}', "
            f"linked_player_role: '{const.linked_player_role}'."
        )
        print("------")
        print("Bot is ready!")
        print("------")

    _ = on_ready  # Silence unaccessed function warni
