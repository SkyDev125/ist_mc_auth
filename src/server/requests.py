import aiohttp
from src.db.player import *


async def add_player_to_whitelist(player: ISTPlayer | InvitedPlayer) -> None:
    """Adds the player to the whitelist asynchronously."""
    if not player["minecraft_name"]:
        print("Player has no Minecraft name. Cannot add to whitelist.")
        return

    uuid = await fetch_uuid_async(player["minecraft_name"])

    if not uuid:
        print(
            f"Player {player['minecraft_name']} does not exist. Cannot add to whitelist."
        )
        return

    url = "http://eu-de-1.arthmc.xyz:11095/v1/server/whitelist"
    headers = {
        "accept": "application/json",
        "key": "16$2!LBaQre39B*MT4MHSeOe8Vaji3",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"uuid": uuid, "name": player["minecraft_name"]}

    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, headers=headers, data=data) as response:
            if response.status != 200:
                raise Exception(
                    f"Failed to add player to whitelist. Status: {response.status}"
                )


async def remove_player_from_whitelist(player: ISTPlayer | InvitedPlayer) -> None:
    """Removes the player from the whitelist asynchronously."""
    if not player["minecraft_name"]:
        print("Player has no Minecraft name. Cannot remove from whitelist.")
        return

    uuid = await fetch_uuid_async(player["minecraft_name"])

    if not uuid:
        print(
            f"Player {player['minecraft_name']} does not exist. Cannot remove from whitelist."
        )
        return

    url = "http://eu-de-1.arthmc.xyz:11095/v1/server/whitelist"
    headers = {
        "accept": "application/json",
        "key": "16$2!LBaQre39B*MT4MHSeOe8Vaji3",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"uuid": uuid, "name": player["minecraft_name"]}

    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.delete(url, headers=headers, data=data) as response:
            if response.status != 200:
                print(
                    f"Failed to remove player from whitelist. Status: {response.status}"
                )
                text = await response.text()
                print(f"Response: {text}")


async def fetch_uuid_async(username: str) -> str | None:
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    timeout = aiohttp.ClientTimeout(total=5)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                raw_uuid = data["id"]
                formatted_uuid = f"{raw_uuid[:8]}-{raw_uuid[8:12]}-{raw_uuid[12:16]}-{raw_uuid[16:20]}-{raw_uuid[20:]}"
                return formatted_uuid
            elif response.status == 204:
                print(f"Username '{username}' not found.")
                return None
            else:
                print(f"Failed to fetch UUID. Status: {response.status}")
                return None
