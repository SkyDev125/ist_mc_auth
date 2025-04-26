from typing import Any, TypeGuard, TypedDict, List

class ISTPlayer(TypedDict):
    id: str                     # ist_id
    discord_id: str
    minecraft_name: str | None
    invited_ids: List[str]
    invite_limit: int


class InvitedPlayer(TypedDict):
    id: str
    discord_id: str
    minecraft_name: str | None
    invited_by: str             # ist_id of inviter

def is_ist_player(player: Any) -> TypeGuard[ISTPlayer]:
    return isinstance(player, dict) and "invite_limit" in player

def is_invited_player(player: Any) -> TypeGuard[InvitedPlayer]:
    return isinstance(player, dict) and "invited_by" in player