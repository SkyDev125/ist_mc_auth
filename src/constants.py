import discord

# Message constants
DEFAULT_MESSAGE_DELETE_DELAY = 120

# Server constants
MAX_INVITES = 5

# Guild constants
GUILD_ID = 1346582307783577635
# This is assigned once at runtime and should be treated as constant after assignment.
guild: discord.Guild | None = None

# Guild Roles
IST_PLAYER_ROLE_ID = 1359003671031054458
GUEST_PLAYER_ROLE_ID = 1359003727029338284
LINKED_PLAYER_ROLE_ID = 1359013493923123311
# These are assigned once at runtime and should be treated as constants after assignment.
ist_player_role: discord.Role | None = None
guest_player_role: discord.Role | None = None
linked_player_role: discord.Role | None = None
