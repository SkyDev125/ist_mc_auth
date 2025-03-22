import importlib.util
import importlib
from discord.ext.commands import Bot
from pathlib import Path
from beartype import beartype


@beartype
def load_all_from(folder: Path, bot: Bot, is_event: bool = False) -> None:
    for file in folder.glob("*.py"):
        if file.name.startswith("_"):
            continue  # skip __init__.py or _private.py

        module_name = f"{folder.name}.{file.stem}"
        module = importlib.import_module(f"src.{module_name}")

        if hasattr(module, "setup"):
            module.setup(bot)
        elif is_event:
            raise AttributeError(f"{file.name} is missing a `setup(bot)` function")
