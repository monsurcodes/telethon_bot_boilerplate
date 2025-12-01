from telethon import TelegramClient
from bot.config import API_ID, API_HASH, BOT_TOKEN
from bot.core.dispatcher import Dispatcher
from bot.helpers.plugin_loader import discover_plugins
from bot.helpers.logger import get_logger

logger = get_logger(__name__)

class TelethonBot:

    def __init__(self, session_name="telethon_bot"):
        logger.info("Initializing Telethon client.")
        self.client = TelegramClient(session_name, API_ID, API_HASH)
        self.BOT_USERNAME = None
        logger.info("Telethon client started.")
        self.dispatcher = Dispatcher(self.client)
        self.plugins = []

    async def start(self):
        await self.client.start(bot_token=BOT_TOKEN)
        me = await self.client.get_me()
        self.BOT_USERNAME = me.username
        self.load_plugins()
        logger.info(f"Bot started successfully as @{self.BOT_USERNAME}!")

    def load_plugins(self):
        import bot.plugins
        plugin_classes = discover_plugins(bot.plugins)

        for plugin_cls in plugin_classes:
            plugin_instance = plugin_cls(self)
            plugin_instance.register()
            self.plugins.append(plugin_instance)
            logger.info(f"Loaded plugin: {plugin_instance.__class__.__module__}.{plugin_instance.__class__.__name__}")

    def run(self):
        self.client.loop.run_until_complete(self.start())
        self.client.run_until_disconnected()
