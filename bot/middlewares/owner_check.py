from functools import wraps
from bot.config import OWNER_ID

def owner_only(handler_func):
    @wraps(handler_func)
    async def wrapper(self, event, *args, **kwargs):
        sender = await event.get_sender()
        if int(sender.id) == int(OWNER_ID):
            return await handler_func(self, event, *args, **kwargs)
        else:
            await event.reply("**⚠️ Unauthorized access**: Only the bot owner can use this command.")
    return wrapper
