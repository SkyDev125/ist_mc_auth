from discord.ext.commands import Bot
from pathlib import Path
from src.utils.autoload import load_all_from


def load_events(bot: Bot) -> None:
    load_all_from(Path(__file__).parent, bot, is_event=True)
