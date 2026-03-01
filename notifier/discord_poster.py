"""
notifier/discord_poster.py — Discord HTTP API poster

Posts alerts directly to Discord channels via bot token.
No subprocess shenanigans — pure urllib.
"""
import json
import logging
import urllib.request
import urllib.error
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import DISCORD_BOT_TOKEN, DISCORD_EARLY_TRENDING_CHANNEL, DISCORD_RUNNERS_CHANNEL

logger = logging.getLogger(__name__)

DISCORD_API = "https://discord.com/api/v10/channels/{}/messages"


class DiscordPoster:
    def __init__(self, bot_token: str = None):
        self.token = bot_token or DISCORD_BOT_TOKEN
        if not self.token:
            logger.warning("No Discord bot token configured!")

    def _send(self, channel_id: str, content: str) -> bool:
        """Send a message to a Discord channel. Returns True on success."""
        if not self.token:
            logger.error("Cannot send to Discord: no bot token")
            return False

        url = DISCORD_API.format(channel_id)
        # Discord max 2000 chars per message
        if len(content) > 1990:
            content = content[:1990] + "…"

        payload = json.dumps({"content": content}).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Authorization": f"Bot {self.token}",
                "Content-Type": "application/json",
                "User-Agent": "HypeScout/2.0",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.status in (200, 201)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            logger.error(f"Discord HTTP {e.code}: {body}")
            return False
        except Exception as e:
            logger.error(f"Discord send error: {e}")
            return False

    def post_alert(self, content: str) -> bool:
        """Post a token alert to the early-trending channel."""
        return self._send(DISCORD_EARLY_TRENDING_CHANNEL, content)

    def post_runner(self, content: str) -> bool:
        """Post a pump runner alert to the runners channel."""
        return self._send(DISCORD_RUNNERS_CHANNEL, content)

    def post_to(self, channel_id: str, content: str) -> bool:
        """Post to any arbitrary channel ID."""
        return self._send(channel_id, content)
