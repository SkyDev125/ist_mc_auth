"""
Custom exceptions for database operations.
These exceptions provide more specific error types than generic exceptions
to allow for better error handling in the application.
"""

from typing import Optional


class DatabaseError(Exception):
    """Base class for all database-related exceptions."""

    pass


class PlayerNotFoundError(DatabaseError):
    """Raised when a player cannot be found in the database."""

    def __init__(self, player_id: str, message: Optional[str] = None):
        self.player_id = player_id
        self.message = message or f"Player with ID '{player_id}' not found."
        super().__init__(self.message)


class InsertError(DatabaseError):
    """Raised when inserting a player into the database fails."""

    def __init__(self, player_type: str, message: Optional[str] = None):
        self.player_type = player_type
        self.message = message or f"Failed to add {player_type} player to the database."
        super().__init__(self.message)


class UpdateError(DatabaseError):
    """Raised when updating a player in the database fails."""

    def __init__(self, player_id: str, player_type: str, message: Optional[str] = None):
        self.player_id = player_id
        self.player_type = player_type
        self.message = (
            message or f"Failed to update {player_type} player with ID '{player_id}'."
        )
        super().__init__(self.message)


class DeleteError(DatabaseError):
    """Raised when deleting a player from the database fails."""

    def __init__(self, player_id: str, player_type: str, message: Optional[str] = None):
        self.player_id = player_id
        self.player_type = player_type
        self.message = (
            message or f"Failed to delete {player_type} player with ID '{player_id}'."
        )
        super().__init__(self.message)


class SearchError(DatabaseError):
    """Raised when a search operation fails or returns no results."""

    def __init__(
        self, search_field: str, search_value: str, message: Optional[str] = None
    ):
        self.search_field = search_field
        self.search_value = search_value
        self.message = (
            message or f"No players found with {search_field} '{search_value}'."
        )
        super().__init__(self.message)


class DatabaseConnectionError(DatabaseError):
    """Raised when there's an issue connecting to the database."""

    def __init__(self, message: Optional[str] = None):
        self.message = message or "Failed to connect to the database."
        super().__init__(self.message)


class DatabaseInitializationError(DatabaseError):
    """Raised when there's an issue initializing the database."""

    def __init__(self, message: Optional[str] = None):
        self.message = message or "Failed to initialize the database."
        super().__init__(self.message)


class PlayerAlreadyExistsError(DatabaseError):
    """Raised when trying to add a player that already exists in the database."""

    def __init__(self, player_id: str, message: Optional[str] = None):
        self.player_id = player_id
        self.message = message or f"Player with ID '{player_id}' already exists."
        super().__init__(self.message)
