from asyncio import Lock
import asyncio
import os
import secrets

# import aiohttp
from aiohttp import web
import aiohttp
from beartype import beartype
from discord.ext import commands
from typing import Optional
import discord
from src.db.db import db
from src.db.player import ISTPlayer

# --- Configuration (Replace with your actual values, consider using environment variables) ---
FENIX_CLIENT_ID = os.getenv("FENIX_CLIENT_ID")
FENIX_CLIENT_SECRET = os.getenv("FENIX_CLIENT_SECRET")
AUTH_TIMEOUT_SECONDS = os.getenv("AUTH_TIMEOUT_SECONDS")
# Make sure this matches the Redirect URL in your FenixEdu application registration
FENIX_REDIRECT_URI = "http://localhost:8080/callback"
FENIX_BASE_URL = "https://fenix.tecnico.ulisboa.pt"
ACCESS_TOKEN_PATH = "/oauth/access_token"
PERSON_API_PATH = "/api/fenix/v1/person"
TIMEOUT = 10
# --- End Configuration ---

auth_connections: dict[str, discord.Interaction] = {}  # auth_id-interaction linker
auth_connections_lock = Lock()

runner: Optional[web.AppRunner] = None  # Global variable to hold the web server runner


async def create_auth_url(interaction: discord.Interaction) -> str:
    """Creates the authorization URL for FenixEdu OAuth."""
    auth_id = secrets.token_urlsafe(16)

    auth_url = f"{FENIX_BASE_URL}/oauth/userdialog?client_id={FENIX_CLIENT_ID}&redirect_uri={FENIX_REDIRECT_URI}&state={auth_id}"

    # add the state to the auth_connections dictionary TODO: add
    async with auth_connections_lock:
        auth_connections[auth_id] = interaction

    return auth_url


async def exchange_code_for_token(
    auth_code: str, session: aiohttp.ClientSession
) -> dict[str, str] | None:
    """
    Exchanges an authorization code for an access token and refresh token.

    Args:
        auth_code: The authorization code received from the FenixEdu callback.
        session: An active aiohttp.ClientSession instance.

    Returns:
        A dictionary containing token information (access_token, refresh_token,
        expires_in, etc.) if successful, None otherwise.
    """
    if not auth_code:
        print("ERROR: exchange_code_for_token called without an authorization code.")
        return None

    token_url = f"{FENIX_BASE_URL}{ACCESS_TOKEN_PATH}"
    # Use base registered URI for token exchange based on Fenix docs example
    redirect_uri_for_exchange = FENIX_REDIRECT_URI.split("?")[0]

    token_payload = {
        "client_id": FENIX_CLIENT_ID,
        "client_secret": FENIX_CLIENT_SECRET,
        "redirect_uri": redirect_uri_for_exchange,
        "code": auth_code,
        "grant_type": "authorization_code",
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    try:
        timeout = aiohttp.ClientTimeout(total=TIMEOUT)
        async with session.post(
            token_url, data=token_payload, headers=headers, timeout=timeout
        ) as response:
            if response.status == 200:
                try:
                    token_data = await response.json()
                    return token_data
                except aiohttp.ContentTypeError:
                    resp_text = await response.text()
                    print(
                        f"Failed to decode JSON response from {token_url}. Response: {resp_text[:200]}"
                    )
                    return None
            else:
                error_details = await response.text()
                print(
                    f"Failed to exchange code for token. Status: {response.status}, Details: {error_details[:200]}"
                )
                return None
    except asyncio.TimeoutError:
        print(f"ERROR: Request to {token_url} timed out during code exchange.")
        return None
    except aiohttp.ClientError as e:
        print(f"ERROR: Network or HTTP error during code exchange: {e}")
        return None
    except Exception as e:
        print(f"ERROR: Unexpected error during code exchange: {e}")
        return None


async def get_fenix_user_info(
    access_token: str, session: aiohttp.ClientSession
) -> dict[str, str] | None:
    """
    Fetches user information from the FenixEdu /person API endpoint.

    Args:
        access_token: The valid OAuth 2.0 access token for the user.
        session: An active aiohttp.ClientSession instance.

    Returns:
        A dictionary containing the user's information if successful, None otherwise.
        The 'username' field typically holds the IST ID (e.g., istXXXXXX).
    """
    if not access_token:
        print("get_fenix_user_info called without an access token.")
        return None

    target_url = f"{FENIX_BASE_URL}{PERSON_API_PATH}"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        timeout = aiohttp.ClientTimeout(total=TIMEOUT)
        async with session.get(
            target_url, headers=headers, timeout=timeout
        ) as response:
            if response.status == 200:
                try:
                    person_data = await response.json()
                    return person_data
                except aiohttp.ContentTypeError:
                    resp_text = await response.text()
                    print(
                        f"Failed to decode JSON response from {target_url}. Response: {resp_text[:200]}"
                    )
                    return None
            else:
                error_details = await response.text()
                print(
                    f"Failed to fetch user info. Status: {response.status}, Details: {error_details[:200]}"
                )
                return None
    except asyncio.TimeoutError:
        print(f"Request to {target_url} timed out.")
        return None
    except aiohttp.ClientError as e:
        print(f"Network or HTTP error fetching user info: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error fetching user info: {e}")
        return None


async def handle_callback(request: web.Request) -> web.Response:
    """Handles the OAuth callback from FenixEdu."""
    # Set html content for response
    html_content1 = """
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        text-align: center;
                        margin-top: 50px;
                    }}
                    h1 {{
                        color: #333;
                    }}
                    p {{
                        font-size: 18px;
                    }}
                    #countdown {{
                        font-weight: bold;
                        color: red;
                    }}
                </style>
                <title>Authentication Callback</title>
                <script>
                    let timeLeft = 10;
                    function updateCountdown() {{
                        document.getElementById('countdown').textContent = timeLeft;
                        if (timeLeft == 0) {{
                            window.close();
                        }} else {{
                            timeLeft--;
                            setTimeout(updateCountdown, 1000);
                        }}
                    }}
                    window.onload = updateCountdown;
                </script>
            </head>
            <body>
                <h1>Authentication Callback Received</h1>
                <p>"""

    result = "Authentication successful!"

    html_content2 = """This window will close in <span id="countdown">5</span> seconds.</p>
            </body>
        </html>
    """

    # Extract parameters from query
    auth_code = request.query.get("code", None)
    auth_id = request.query.get("state", None)

    if not auth_code or not auth_id:
        print("Callback received without code or state.")
        result = "Invalid Callback Parameters... Contact the server admins."
        return web.Response(
            text=html_content1 + result + html_content2, content_type="text/html"
        )

    # Check if the auth_id is valid and retrieve the interaction
    interaction = None
    async with auth_connections_lock:
        interaction = auth_connections.pop(auth_id, None)

    if not interaction:
        print("No interaction found for the provided auth_id.")
        result = "Interaction Missing... Contact the server admins."
        return web.Response(
            text=html_content1 + result + html_content2, content_type="text/html"
        )

    # Gather user info from FenixEdu
    async with aiohttp.ClientSession() as session:
        token_result = await exchange_code_for_token(auth_code, session)
        if not token_result:
            print("Token exchange failed. No result returned.")
            result = "Token exchange failed."
            await interaction.user.send(
                "Failed to authenticate. Please try again. \n\n if the problem persists, contact the server admins.",
                delete_after=120,
            )
            return web.Response(
                text=html_content1 + result + html_content2, content_type="text/html"
            )

        user_info = await get_fenix_user_info(token_result["access_token"], session)
        if not user_info:
            print("Failed to fetch user info. No result returned.")
            result = "Failed to fetch user info."
            await interaction.user.send(
                "Failed to authenticate. Please try again. \n\n if the problem persists, contact the server admins.",
                delete_after=120,
            )
            return web.Response(
                text=html_content1 + result + html_content2, content_type="text/html"
            )

        # add the user to the database
        ist_player = ISTPlayer(
            id=user_info["username"],
            discord_id=str(interaction.user.id),
            minecraft_name=None,
            invited_ids=[],
            invite_limit=5,
        )

        try:
            db.add_ist(ist_player)
        except Exception as e:
            print(f"Failed to add IST player to the database: {e}")
            result = f"Failed to add IST player to the database: {e} \n\n If you think this is a mistake, please contact the server admins."
            await interaction.user.send(result, delete_after=120)
            return web.Response(
                text=html_content1 + result + html_content2,
                content_type="text/html",
            )

        await interaction.user.send(
            "Authentication successful! Welcome to the server!\n\n"
            "Use /link to link your Minecraft account if you want to play on the server.",
            delete_after=120,
        )

    # Return the response
    return web.Response(
        text=html_content1 + result + html_content2, content_type="text/html"
    )


# TODO: Update the URL to use a domain instead of localhost when deployed.
@beartype
async def start_server(bot: commands.Bot) -> None:
    """Starts the AIOHTTP web server."""
    if not FENIX_CLIENT_ID or not FENIX_REDIRECT_URI:
        raise ValueError(
            "FENIX_CLIENT_ID and FENIX_REDIRECT_URI must be set and not None."
        )

    app = web.Application()
    app["bot"] = bot  # Make bot accessible in handlers
    app.router.add_get("/callback", handle_callback)

    runner = web.AppRunner(app)
    await runner.setup()
    # Extract host and port from REDIRECT_URI for binding
    # Basic parsing, assumes http://host:port/path format
    try:
        from urllib.parse import urlparse

        parsed_uri = urlparse(FENIX_REDIRECT_URI)
        host = parsed_uri.hostname or "localhost"
        port = parsed_uri.port or 8080  # Default port if not specified
    except Exception:
        host = "localhost"
        port = 8080
        print(
            f"Warning: Could not parse REDIRECT_URI ('{FENIX_REDIRECT_URI}'). Defaulting server to {host}:{port}"
        )

    site = web.TCPSite(runner, host, port)
    await site.start()
    print(f"Web server started on {host}:{port}")


@beartype
async def stop_server() -> None:
    """Stops the AIOHTTP web server."""
    if runner is None:
        print("Web server is not running.")
        return

    await runner.cleanup()
    print("Web server stopped.")
