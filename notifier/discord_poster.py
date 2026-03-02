"""
notifier/discord_poster.py — Discord HTTP API poster

Posts alerts directly to Discord channels via bot token.
No subprocess shenanigans — pure urllib.
"""
import json
import logging
import requests
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

    def _send(self, channel_id: str, content: str) -> str | None:
        """Send a message to a Discord channel. Returns message ID on success, None on failure."""
        if not self.token:
            logger.error("Cannot send to Discord: no bot token")
            return None

        url = DISCORD_API.format(channel_id)
        if len(content) > 1990:
            content = content[:1990] + "…"
        try:
            resp = requests.post(url, json={"content": content}, headers={
                "Authorization": f"Bot {self.token}",
                "User-Agent": "HypeScout/2.0",
            }, timeout=15)
            if resp.ok:
                return resp.json().get("id")
            logger.error(f"Discord HTTP {resp.status_code}: {resp.text}")
            return None
        except Exception as e:
            logger.error(f"Discord send error: {e}")
            return None

    def pin_message(self, channel_id: str, message_id: str) -> bool:
        """Pin a message in a channel. Returns True on success."""
        try:
            resp = requests.put(
                f"https://discord.com/api/v10/channels/{channel_id}/pins/{message_id}",
                headers={"Authorization": f"Bot {self.token}", "Content-Length": "0"},
                timeout=10,
            )
            return resp.status_code in (200, 204)
        except Exception as e:
            logger.error(f"Discord pin error: {e}")
            return False

    def unpin_message(self, channel_id: str, message_id: str) -> bool:
        """Unpin a message in a channel. Returns True on success."""
        try:
            resp = requests.delete(
                f"https://discord.com/api/v10/channels/{channel_id}/pins/{message_id}",
                headers={"Authorization": f"Bot {self.token}"},
                timeout=10,
            )
            return resp.status_code in (200, 204)
        except Exception as e:
            logger.error(f"Discord unpin error: {e}")
            return False

    def _send_embed(self, channel_id: str, content: str, image_url: str = "") -> str | None:
        """Send a Discord embed with optional thumbnail. Falls back to plain text if embed fails."""
        if not self.token:
            return None
        url = DISCORD_API.format(channel_id)
        embed = {
            "description": content[:4096],
            "color": 0x00E676,  # bright green accent
        }
        if image_url:
            embed["thumbnail"] = {"url": image_url}
        try:
            resp = requests.post(url, json={"embeds": [embed]}, headers={
                "Authorization": f"Bot {self.token}",
                "User-Agent": "HypeScout/2.0",
            }, timeout=15)
            if resp.ok:
                return resp.json().get("id")
            # Embed failed (e.g. bad image URL) — fall back to plain text
            logger.warning(f"Discord embed {resp.status_code}, falling back to text")
            return self._send(channel_id, content)
        except Exception as e:
            logger.error(f"Discord embed error: {e}")
            return self._send(channel_id, content)

    def post_alert(self, content: str, image_url: str = "") -> str | None:
        """Post a token alert to the early-trending channel. Returns message ID."""
        if image_url:
            return self._send_embed(DISCORD_EARLY_TRENDING_CHANNEL, content, image_url)
        return self._send(DISCORD_EARLY_TRENDING_CHANNEL, content)

    def post_runner(self, content: str) -> str | None:
        """Post a pump runner alert to the runners channel. Returns message ID."""
        return self._send(DISCORD_RUNNERS_CHANNEL, content)

    def post_to(self, channel_id: str, content: str) -> str | None:
        """Post to any arbitrary channel ID. Returns message ID."""
        return self._send(channel_id, content)
