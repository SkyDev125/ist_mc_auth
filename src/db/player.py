from typing import TypedDict, List

class ISTPlayer(TypedDict):
    id: str                     # ist_id
    discord_id: str
    minecraft_name: str | None
    invited_ids: List[str]
    invite_limit: int


class InvitedPlayer(TypedDict):
    id: str
    discord_id: str
    minecraft_name: str
    invited_by: str             # ist_id of inviter
