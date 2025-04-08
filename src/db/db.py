import os
from tinydb import TinyDB, Query
from typing import cast
from src.errors.db import *
from src.db.player import ISTPlayer, InvitedPlayer

DB_PATH = os.path.join(os.path.dirname(__file__), "data","players.json")


class Database:
    def __init__(self):
        if not os.path.exists(DB_PATH):
            with open(DB_PATH, "x") as f:
                f.write("")

        # Initialize the database
        self.db = TinyDB(DB_PATH)

        # Initialize the tables
        self.ist_players = self.db.table(  # pyright: ignore[reportUnknownMemberType]
            "ist_players"
        )
        self.invited_players = self.db.table(  # pyright: ignore[reportUnknownMemberType]
            "invited_players"
        ) 

        # Initialize the query object
        self.query = Query()

    # --------------------------
    # 👥 IST PLAYERS
    # --------------------------
    def add_ist(self, ist_player: ISTPlayer) -> None:
        """Add IST player to the database."""
        if self.ist_players.contains(self.query.id == ist_player["id"]):
            raise PlayerAlreadyExistsError(ist_player["id"])

        result = self.ist_players.insert(  # pyright: ignore[reportUnknownMemberType]
            ist_player
        )
        if not result:
            raise InsertError("IST")

    def get_ist(self, ist_id: str) -> ISTPlayer:
        """Get IST player by ID."""
        result = self.ist_players.get(  # pyright: ignore[reportUnknownMemberType]
            self.query.id == ist_id
        )
        if result:
            return cast(ISTPlayer, result)
        raise PlayerNotFoundError(ist_id)

    def get_all_ist(self) -> list[ISTPlayer]:
        """Get all IST players."""
        results = self.ist_players.all()
        if results:
            return [cast(ISTPlayer, result) for result in results]
        raise PlayerNotFoundError("", message="No IST players found")

    def update_ist(self, ist_player: ISTPlayer) -> None:
        """Update IST player in the database."""
        result = self.ist_players.update(  # pyright: ignore[reportUnknownMemberType]
            ist_player, self.query.id == ist_player["id"]
        )
        if not result:
            raise UpdateError(ist_player["id"], "IST")

    def delete_ist(self, ist_id: str) -> None:
        """Delete IST player from the database."""
        result = self.ist_players.remove(self.query.id == ist_id)
        if not result:
            raise DeleteError(ist_id, "IST")

    # --------------------------
    # 👥 INVITED PLAYERS
    # --------------------------
    def add_invited(self, invited_player: InvitedPlayer) -> None:
        """Add invited player to the database."""
        if self.invited_players.contains(self.query.id == invited_player["id"]):
            raise PlayerAlreadyExistsError(invited_player["id"])

        result = (
            self.invited_players.insert(  # pyright: ignore[reportUnknownMemberType]
                invited_player
            )
        )
        if not result:
            raise InsertError("Invited")

    def get_invited(self, invited_id: str) -> InvitedPlayer:
        """Get invited player by ID."""
        result = self.invited_players.get(  # pyright: ignore[reportUnknownMemberType]
            self.query.id == invited_id
        )
        if result:
            return cast(InvitedPlayer, result)
        raise PlayerNotFoundError(invited_id)

    def get_all_invited(self) -> list[InvitedPlayer]:
        """Get all invited players."""
        results = self.invited_players.all()
        if results:
            return [cast(InvitedPlayer, result) for result in results]
        raise PlayerNotFoundError("", message="No invited players found")

    def update_invited(self, invited_player: InvitedPlayer) -> None:
        """Update invited player in the database."""
        result = (
            self.invited_players.update(  # pyright: ignore[reportUnknownMemberType]
                invited_player, self.query.id == invited_player["id"]
            )
        )
        if not result:
            raise UpdateError(invited_player["id"], "Invited")

    def delete_invited(self, invited_id: str) -> None:
        """Delete invited player from the database."""
        result = self.invited_players.remove(self.query.id == invited_id)
        if not result:
            raise DeleteError(invited_id, "Invited")

    # --------------------------
    # 🔍 SEARCH
    # --------------------------
    def search_minecraft_name(self, name: str) -> ISTPlayer | InvitedPlayer:
        """Search for IST players by Minecraft name."""
        results = self.ist_players.search(self.query.minecraft_name == name)
        if results:
            return cast(ISTPlayer, results[0])
        results = self.invited_players.search(self.query.minecraft_name == name)
        if results:
            return cast(InvitedPlayer, results[0])
        raise SearchError("minecraft_name", name)

    def search_discord_id(self, discord_id: str) -> ISTPlayer | InvitedPlayer:
        """Search for IST players by Discord ID."""
        results = self.ist_players.search(self.query.discord_id == discord_id)
        if results:
            return cast(ISTPlayer, results[0])
        results = self.invited_players.search(self.query.discord_id == discord_id)
        if results:
            return cast(InvitedPlayer, results[0])
        raise SearchError("discord_id", discord_id)


# Global instance for import
db = Database()
