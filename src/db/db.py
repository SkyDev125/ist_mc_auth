from db.player import *
import os
from tinydb import TinyDB, Query
from typing import cast
from errors.db import *

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "players.json")

class Database:
    def __init__(self):
        if not os.path.exists(DB_PATH):
            with open(DB_PATH, 'w') as f:
                f.write('{}')
        
        # Initialize the database
        self.db = TinyDB(DB_PATH)
        
        # Initialize the tables
        self.ist_players = self.db.table('ist_players') # pyright: ignore[reportUnknownMemberType]
        self.invited_players = self.db.table('invited_players') # pyright: ignore[reportUnknownMemberType]
        
        # Initialize the query object
        self.query = Query()
    
    
    # --------------------------
    # 👥 IST PLAYERS
    # --------------------------
    def add_ist(self, ist_player: ISTPlayer) -> None:
        """Add IST player to the database."""
        result = self.ist_players.insert(ist_player) # pyright: ignore[reportUnknownMemberType]
        if result:
            return
        raise InsertError("IST")

    def get_ist(self, ist_id: str) -> ISTPlayer:
        """Get IST player by ID."""
        result = self.ist_players.get(self.query.id == ist_id) # pyright: ignore[reportUnknownMemberType]
        if result:
            return cast(ISTPlayer, result)
        raise PlayerNotFoundError(ist_id)
    
    def get_all_ist(self) -> list[ISTPlayer]:
        """Get all IST players."""
        results = self.ist_players.all()
        if results:
            return [cast(ISTPlayer, result) for result in results]
        raise PlayerNotFoundError("",message="No IST players found")
    
    def update_ist(self, ist_player: ISTPlayer) -> None:
        """Update IST player in the database."""
        result = self.ist_players.update(ist_player, self.query.id == ist_player['id'])  # pyright: ignore[reportUnknownMemberType]
        if result:
            return
        raise UpdateError(ist_player['id'], "IST")
    
    def delete_ist(self, ist_id: str) -> None:
        """Delete IST player from the database."""
        result = self.ist_players.remove(self.query.id == ist_id)
        if result:
            return
        raise DeleteError(ist_id, "IST")
    
    
    # --------------------------
    # 👥 INVITED PLAYERS
    # --------------------------
    def add_invited(self, invited_player: InvitedPlayer) -> None:
        """Add invited player to the database."""
        result = self.invited_players.insert(invited_player) # pyright: ignore[reportUnknownMemberType]
        if result:
            return 
        raise InsertError("Invited")
    
    def get_invited(self, invited_id: str) -> InvitedPlayer:
        """Get invited player by ID."""
        result = self.invited_players.get(self.query.id == invited_id) # pyright: ignore[reportUnknownMemberType]
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
        result = self.invited_players.update(invited_player, self.query.id == invited_player['id']) # pyright: ignore[reportUnknownMemberType]
        if result:
            return
        raise UpdateError(invited_player['id'], "Invited")
    
    def delete_invited(self, invited_id: str) -> None:
        """Delete invited player from the database."""
        result = self.invited_players.remove(self.query.id == invited_id)
        if result:
            return
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