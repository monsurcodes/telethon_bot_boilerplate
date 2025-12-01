from telethon import events, Button

from bot.constants import START_MESSAGE
from bot.core.base_plugin import BasePlugin
from bot.helpers.command_patterns import command_pattern
from bot.helpers.logger import get_logger

logger = get_logger(__name__)


class StartPlugin(BasePlugin):

    def register(self):
        self.bot.dispatcher.register_handler(
            self.on_start_command,
            events.NewMessage(pattern=command_pattern('start'))
        )
        self.bot.dispatcher.register_handler(self.on_start_callback, events.CallbackQuery)

    async def on_start_command(self, event: events.NewMessage.Event):
        try:
            user = await event.get_sender()

            user_buttons = [
                [Button.inline("Commands ❓", f"show_commands"), Button.url("Dev 👨‍💻", "https://t.me/minkxx69")],
                [Button.url("Repo 🛠️", "https://github.com/monsurcodes/telethon_bot_boilerplate")],
                [Button.url("Add Me To Your Group 🎉", f"https://t.me/{self.bot.BOT_USERNAME}?startgroup=new")],
            ]

            await event.reply(
                START_MESSAGE.format(user.first_name),
                buttons=user_buttons,
                parse_mode="md"
            )
        except Exception as e:
            logger.exception(e)
            await event.reply("Failed to send start message. Check bot logs for details.")

    async def on_start_callback(self, event: events.CallbackQuery.Event):
        data = event.data.decode()
        if data.startswith("show_commands"):
            await event.respond("Click /help to see the list of commands")
            await event.answer()
