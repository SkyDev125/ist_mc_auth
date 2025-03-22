from discord.ext.commands import Bot
from pathlib import Path
from src.utils.autoload import load_all_from
from beartype import beartype


@beartype
def load_commands(bot: Bot) -> None:
    load_all_from(Path(__file__).parent, bot)
