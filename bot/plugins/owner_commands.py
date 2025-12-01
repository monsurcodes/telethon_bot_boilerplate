import platform
import sys

import psutil
from telethon import __version__ as telethon_version
from telethon import events

from bot.core.base_plugin import BasePlugin
from bot.middlewares.owner_check import owner_only
from bot.helpers.command_patterns import command_pattern
from bot.helpers.logger import get_logger

logger = get_logger(__name__)


class OwnerPlugin(BasePlugin):
    name = "Owner"

    def register(self):

        self.bot.dispatcher.register_handler(self.on_sendlogs_command, events.NewMessage(pattern=command_pattern('logs')))
        self.bot.dispatcher.register_handler(self.stats_command, events.NewMessage(pattern=command_pattern("stats")))

    @owner_only
    async def on_sendlogs_command(self, event: events.NewMessage.Event):
        try:
            user = await event.get_sender()

            await self.bot.client.send_file(
                user.id,
                file="logs/bot.log",
                caption="Bot logs!"
            )

            await event.reply(f"Sent log to {user.first_name}!")
        except Exception as e:
            logger.exception(e)
            await event.reply("Failed to send logs. Check bot logs for details.")

    @owner_only
    async def stats_command(self, event: events.NewMessage.Event):
        try:
            # Get system info
            tele_version = telethon_version
            python_version = sys.version.split()[0]
            platform_info = f"{platform.system()} {platform.release()} ({platform.machine()})"
            ram = psutil.virtual_memory()
            ram_used_mb = ram.used // (1024 * 1024)
            ram_total_mb = ram.total // (1024 * 1024)
            ram_percent = ram.percent
            cpu_percent = psutil.cpu_percent(interval=0.5)


            text = (
                "📊 **Bot Stats:**\n\n"
                f"🤖 **Telethon:** `{tele_version}`\n"
                f"🐍 **Python:** `{python_version}`\n"
                f"💻 **System:** `{platform_info}`\n"
                f"🧠 **RAM Usage:** `{ram_used_mb} MB` / `{ram_total_mb} MB` ({ram_percent}%)\n"
                f"🖥️ **CPU Usage:** `{cpu_percent}%`\n"
            )

            await event.reply(text, parse_mode="md")
        except Exception as e:
            logger.exception(e)
            await event.reply("Failed to get stats. Check bot logs for details.")
