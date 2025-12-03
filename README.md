# Telethon Bot Boilerplate

A clean, modular, and extensible boilerplate for building Telegram bots using the [Telethon](https://github.com/LonamiWebs/Telethon) library. This project provides a solid foundation with plugin architecture, middleware support, and utility helpers to accelerate bot development.

## Overview

**Telethon Bot Boilerplate** is designed to eliminate the repetitive setup work when creating Telegram bots. It provides:

- **Plugin-based architecture**: Automatically discover and load plugins from the `plugins/` directory
- **Middleware system**: Intercept and process events before they reach handlers (e.g., owner verification, rate limiting)
- **Clean separation of concerns**: Core bot logic, plugins, middlewares, and helpers are organized in distinct modules
- **Configuration management**: Environment-based configuration using `.env` files
- **Logging infrastructure**: Built-in logging to both console and file for debugging and monitoring
- **Helper utilities**: Reusable components for command patterns, logging, and plugin discovery

This boilerplate is ideal for developers who want to build feature-rich Telegram bots without reinventing the wheel for common patterns like command routing, access control, and modular plugin loading.

## Features

- ✅ **Automatic Plugin Discovery**: Drop Python files in `bot/plugins/` and they're automatically loaded
- ✅ **Middleware Support**: Decorators for pre-processing events (e.g., `@owner_only`)
- ✅ **Command Pattern Helpers**: Utilities to match commands with or without bot username mentions
- ✅ **Structured Logging**: Centralized logger with file and console output
- ✅ **Environment Configuration**: Secure credential management via `.env`
- ✅ **Plugin Enable/Disable**: Control which plugins load via configuration
- ✅ **Example Plugins**: Starter plugins (`start`, `owner_commands`) demonstrating best practices
- ✅ **Event Dispatcher**: Clean abstraction over Telethon's event system


### Directory Purposes

- **`bot/core/`**: Contains the bot's core engine—client initialization, plugin loading, and event dispatcher.
- **`bot/plugins/`**: Add new plugin files here; each plugin defines one or more command/event handlers.
- **`bot/middlewares/`**: Middleware decorators for pre-processing events (authentication, validation, rate limiting).
- **`bot/helpers/`**: Shared utilities like logger setup, command pattern generators, and plugin discovery logic.
- **`bot/config.py`**: Loads environment variables and exposes them as Python constants.
- **`logs/`**: Stores runtime logs (`bot.log`).

## Getting Started

### Prerequisites

- **Python 3.8+**
- **Telegram API credentials** (API ID, API Hash, Bot Token)
- **pip** for dependency management

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/monsurcodes/telethon_bot_boilerplate.git
   cd telethon_bot_boilerplate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. **Obtain Telegram API Credentials**:
   - Visit [https://my.telegram.org/apps](https://my.telegram.org/apps)
   - Log in with your phone number
   - Create a new application to get your `API_ID` and `API_HASH`
   - Create a bot via [@BotFather](https://t.me/BotFather) to get your `BOT_TOKEN`

2. **Create a `.env` file** in the project root:
   ```env
   API_ID=12345678
   API_HASH=0123456789abcdef0123456789abcdef
   BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   OWNER_ID=123456789
   
   # Optional settings
   COMMAND_PREFIX=/
   DISABLED_PLUGINS=
   ```

   **Configuration Options**:
   - `API_ID` (required): Your Telegram API ID from [my.telegram.org](https://my.telegram.org/apps)
   - `API_HASH` (required): Your Telegram API Hash
   - `BOT_TOKEN` (required): Bot token from [@BotFather](https://t.me/BotFather)
   - `OWNER_ID` (required): Your Telegram user ID (for owner-only commands)
   - `COMMAND_PREFIX` (optional): Command prefix, defaults to `/`
   - `DISABLED_PLUGINS` (optional): Comma-separated list of plugin class names to disable (e.g., `StartPlugin,OwnerPlugin`)

3. **Get Your User ID**:
   - Message [@userinfobot](https://t.me/userinfobot) on Telegram to find your user ID
   - Use this ID for the `OWNER_ID` variable

### Running the Bot

**Development Mode**:
```bash
python main.py
```

The bot will:
1. Initialize the Telethon client
2. Authenticate using your bot token
3. Auto-discover and load plugins from `bot/plugins/`
4. Start listening for events
5. Log output to console and `logs/bot.log`

**Production Deployment**:

While this boilerplate doesn't include Docker or systemd configs, you can easily deploy it:

- **Using systemd** (Linux):
  Create a service file at `/etc/systemd/system/telethon-bot.service`:
  ```ini
  [Unit]
  Description=Telethon Bot
  After=network.target

  [Service]
  Type=simple
  User=youruser
  WorkingDirectory=/path/to/telethon_bot_boilerplate
  Environment="PATH=/path/to/venv/bin"
  ExecStart=/path/to/venv/bin/python main.py
  Restart=always

  [Install]
  WantedBy=multi-user.target
  ```
  Then: `sudo systemctl enable telethon-bot && sudo systemctl start telethon-bot`

- **Using Docker**:
  Create a `Dockerfile`:
  ```dockerfile
  FROM python:3.11-slim
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  COPY . .
  CMD ["python", "main.py"]
  ```
  Build and run: `docker build -t telethon-bot . && docker run -d --env-file .env telethon-bot`

## Writing Your Own Plugins

Plugins are the heart of this boilerplate. Each plugin is a Python class that inherits from `BasePlugin` and registers event handlers.

### Plugin Discovery Mechanism

The `plugin_loader.py` helper automatically:
1. Scans all `.py` files in `bot/plugins/`
2. Imports each module
3. Finds classes that inherit from `BasePlugin`
4. Skips plugins listed in `DISABLED_PLUGINS` config
5. Instantiates and calls `.register()` on each plugin

**No manual registration required**—just create a file in `bot/plugins/` with a `BasePlugin` subclass.

### Minimal Plugin Skeleton

Create `bot/plugins/echo.py`:

```python
from telethon import events
from bot.core.base_plugin import BasePlugin
from bot.helpers.command_patterns import command_pattern
from bot.helpers.logger import get_logger

logger = get_logger(__name__)


class EchoPlugin(BasePlugin):
    """Echoes back any message sent to the bot"""

    def register(self):
        # Register event handlers here
        self.bot.dispatcher.register_handler(
            self.on_echo_command,
            events.NewMessage(pattern=command_pattern('echo'))
        )

    async def on_echo_command(self, event: events.NewMessage.Event):
        try:
            # Get the message text
            message = event.message.message
            
            # Send response
            await event.reply(f"You said: {message}")
            
            logger.info(f"Echo command used by {event.sender_id}")
        except Exception as e:
            logger.exception(e)
            await event.reply("Failed to echo message.")
```

### Registering Commands

Use the helper functions in `command_patterns.py`:

```python
from bot.helpers.command_patterns import command_pattern, args_command_pattern

# Match: /start or /start@YourBotName
pattern=command_pattern('start')

# Match: /say hello world (captures "hello world" as group 1)
pattern=args_command_pattern('say')
```

**Example with arguments**:

```python
from bot.helpers.command_patterns import args_command_pattern

class SayPlugin(BasePlugin):
    def register(self):
        self.bot.dispatcher.register_handler(
            self.on_say_command,
            events.NewMessage(pattern=args_command_pattern('say'))
        )

    async def on_say_command(self, event: events.NewMessage.Event):
        # Extract arguments from pattern match
        match = event.pattern_match
        args = match.group(1) if match.group(1) else ""
        
        if not args:
            await event.reply("Usage: /say <text>")
            return
            
        await event.reply(args)
```

### Accessing Shared Services

Inside a plugin, you have access to:

- **`self.bot`**: The main `TelethonBot` instance
- **`self.bot.client`**: The Telethon `TelegramClient` (for API calls)
- **`self.bot.dispatcher`**: Event registration helper
- **`self.bot.BOT_USERNAME`**: The bot's username (set after `start()`)
- **`self.bot.plugins`**: List of loaded plugin instances

**Example—sending a message to the owner**:

```python
from bot.config import OWNER_ID

async def notify_owner(self, message: str):
    await self.bot.client.send_message(OWNER_ID, message)
```

### Error Handling and Logging

Always wrap handler logic in try-except blocks and use the logger:

```python
from bot.helpers.logger import get_logger

logger = get_logger(__name__)

class MyPlugin(BasePlugin):
    async def my_handler(self, event):
        try:
            # Your logic here
            await event.reply("Success!")
            logger.info("Command executed successfully")
        except Exception as e:
            logger.exception(e)  # Logs full traceback
            await event.reply("An error occurred. Check logs.")
```

Logs are written to both console and `logs/bot.log`.

### Example: Full Plugin with Multiple Handlers

```python
from telethon import events, Button
from bot.core.base_plugin import BasePlugin
from bot.helpers.command_patterns import command_pattern
from bot.helpers.logger import get_logger

logger = get_logger(__name__)


class HelpPlugin(BasePlugin):
    """Provides help information"""

    def register(self):
        # Command handler
        self.bot.dispatcher.register_handler(
            self.on_help_command,
            events.NewMessage(pattern=command_pattern('help'))
        )
        # Callback query handler
        self.bot.dispatcher.register_handler(
            self.on_help_callback,
            events.CallbackQuery(pattern=b'help_.*')
        )

    async def on_help_command(self, event: events.NewMessage.Event):
        try:
            buttons = [
                [Button.inline("Commands", b"help_commands")],
                [Button.inline("About", b"help_about")]
            ]
            await event.reply("Choose a help topic:", buttons=buttons)
        except Exception as e:
            logger.exception(e)
            await event.reply("Failed to show help.")

    async def on_help_callback(self, event: events.CallbackQuery.Event):
        data = event.data.decode()
        
        if data == "help_commands":
            await event.edit("Available commands: /start, /help, /echo")
        elif data == "help_about":
            await event.edit("This is a Telethon bot!")
        
        await event.answer()  # Close the loading animation
```

## Middlewares

Middlewares in this boilerplate are **decorator functions** that wrap event handlers to add pre-processing logic (authentication, rate limiting, logging, etc.).

### How Middlewares Work

Middlewares execute **before** the main handler logic. They can:
- Block execution (e.g., if user is unauthorized)
- Modify the event or context
- Log or track event metadata
- Handle errors globally

In this boilerplate, middlewares are applied as decorators to plugin methods.

### Creating a Middleware

A middleware is a decorator function that:
1. Takes a handler function as input
2. Returns a wrapper function
3. The wrapper receives `self`, `event`, and handler args/kwargs

**Example—Admin-only middleware** (`bot/middlewares/admin_check.py`):

```python
from functools import wraps
from bot.config import OWNER_ID

ADMIN_IDS = [OWNER_ID, 987654321]  # Add more admin IDs

def admin_only(handler_func):
    @wraps(handler_func)
    async def wrapper(self, event, *args, **kwargs):
        sender = await event.get_sender()
        if int(sender.id) in ADMIN_IDS:
            return await handler_func(self, event, *args, **kwargs)
        else:
            await event.reply("⚠️ Admin access required.")
    return wrapper
```

**Usage in a plugin**:

```python
from bot.middlewares.admin_check import admin_only

class AdminPlugin(BasePlugin):
    @admin_only
    async def on_ban_command(self, event):
        await event.reply("User banned!")
```

### Built-in Middleware: `owner_only`

Located in `bot/middlewares/owner_check.py`, this middleware restricts commands to the bot owner:

```python
from bot.middlewares.owner_check import owner_only

class OwnerPlugin(BasePlugin):
    def register(self):
        self.bot.dispatcher.register_handler(
            self.on_logs_command,
            events.NewMessage(pattern=command_pattern('logs'))
        )

    @owner_only
    async def on_logs_command(self, event: events.NewMessage.Event):
        # Only OWNER_ID can execute this
        await self.bot.client.send_file(event.sender_id, file="logs/bot.log")
```

If a non-owner tries `/logs`, they receive: *"⚠️ Unauthorized access: Only the bot owner can use this command."*

### Middleware Execution Order

When multiple decorators are stacked, they execute **bottom-up**:

```python
@log_command
@owner_only
async def my_handler(self, event):
    pass
```

Execution order:
1. `log_command` wrapper (outermost)
2. `owner_only` wrapper
3. `my_handler` (if checks pass)

### Advanced: Middleware with Parameters

Create a rate-limiting middleware:

```python
from functools import wraps
from datetime import datetime, timedelta

user_last_command = {}

def rate_limit(seconds=5):
    def decorator(handler_func):
        @wraps(handler_func)
        async def wrapper(self, event, *args, **kwargs):
            user_id = event.sender_id
            now = datetime.now()
            
            if user_id in user_last_command:
                last_time = user_last_command[user_id]
                if now - last_time < timedelta(seconds=seconds):
                    await event.reply(f"⏳ Please wait {seconds} seconds between commands.")
                    return
            
            user_last_command[user_id] = now
            return await handler_func(self, event, *args, **kwargs)
        return wrapper
    return decorator
```

**Usage**:

```python
from bot.middlewares.rate_limit import rate_limit

class SpamPlugin(BasePlugin):
    @rate_limit(seconds=10)
    async def on_spam_command(self, event):
        await event.reply("This command is rate-limited!")
```

### Disabling Middlewares

Middlewares are applied per-handler. To disable, simply don't use the decorator:

```python
# Without middleware—anyone can use
async def on_public_command(self, event):
    await event.reply("Public command!")

# With middleware—owner only
@owner_only
async def on_private_command(self, event):
    await event.reply("Owner command!")
```

## Helpers and Utilities

The `bot/helpers/` directory contains reusable utilities used across plugins and core modules.

### `command_patterns.py`

Generates regex patterns for matching Telegram commands:

- **`command_pattern(cmd)`**: Matches `/cmd` or `/cmd@BotName`
  ```python
  command_pattern('start')  # Matches: /start, /start@MyBot
  ```

- **`args_command_pattern(cmd)`**: Matches commands with optional arguments
  ```python
  args_command_pattern('say')  # Matches: /say, /say hello world
  # Access args via: event.pattern_match.group(1)
  ```

**Customization**: Edit `COMMAND_PREFIX` in `.env` to change the prefix (e.g., `!`, `.`).

### `logger.py`

Provides a configured logger instance:

```python
from bot.helpers.logger import get_logger

logger = get_logger(__name__)

logger.info("Bot started")
logger.warning("Low memory")
logger.error("Failed to connect")
logger.exception(exception_object)  # Logs full traceback
```

**Features**:
- Logs to both console (stdout) and `logs/bot.log`
- Automatic log directory creation
- Timestamp, level, and module name in each log entry
- UTF-8 encoding for international characters

**Log Format**:
```
[2025-12-01 14:32:10,123][INFO][bot.plugins.start] Start command executed
```

### `plugin_loader.py`

Automatically discovers and loads plugins:

```python
from bot.helpers.plugin_loader import discover_plugins
import bot.plugins

plugin_classes = discover_plugins(bot.plugins)
```

**How it works**:
1. Uses `pkgutil.iter_modules()` to find all modules in `bot.plugins`
2. Imports each module dynamically
3. Inspects for `BasePlugin` subclasses
4. Filters out disabled plugins (via `DISABLED_PLUGINS` config)

**Plugin Naming**: Files and class names are flexible—discovery is based on inheritance, not naming conventions.

### Adding New Helpers

To add a new helper (e.g., database wrapper, API client):

1. Create `bot/helpers/database.py`:
   ```python
   import sqlite3
   
   class Database:
       def __init__(self, db_path='bot.db'):
           self.conn = sqlite3.connect(db_path)
           self.cursor = self.conn.cursor()
       
       def get_user(self, user_id):
           self.cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
           return self.cursor.fetchone()
   ```

2. Use in plugins:
   ```python
   from bot.helpers.database import Database
   
   class MyPlugin(BasePlugin):
       def __init__(self, bot):
           super().__init__(bot)
           self.db = Database()
       
       async def my_handler(self, event):
           user = self.db.get_user(event.sender_id)
   ```

## Contributing / Extending

Contributions are welcome! Here's how to extend the boilerplate safely:

### Adding a New Plugin

1. Create a new file in `bot/plugins/` (e.g., `weather.py`)
2. Define a class inheriting from `BasePlugin`
3. Implement the `register()` method
4. Add event handlers using `self.bot.dispatcher.register_handler()`
5. Restart the bot—your plugin will auto-load

### Adding a New Middleware

1. Create a file in `bot/middlewares/` (e.g., `rate_limit.py`)
2. Define a decorator function that wraps async handlers
3. Import and apply the decorator in plugin methods
4. Test with various scenarios (authorized, unauthorized, edge cases)

### Adding a New Helper

1. Create a file in `bot/helpers/` (e.g., `database.py`)
2. Implement reusable functions or classes
3. Document usage in docstrings
4. Import and use in plugins or core modules

### Code Style

- Follow **PEP 8** conventions
- Use **type hints** where applicable (e.g., `event: events.NewMessage.Event`)
- Add **docstrings** to classes and complex functions
- Use the **logger** for debugging, not `print()`

**Recommended tools**:
- `black` for code formatting: `pip install black && black .`
- `flake8` for linting: `pip install flake8 && flake8 bot/`
- `mypy` for type checking: `pip install mypy && mypy bot/`

### Testing

This boilerplate doesn't include tests by default. To add tests:

1. Install `pytest`: `pip install pytest pytest-asyncio`
2. Create `tests/` directory
3. Write test files (e.g., `tests/test_plugins.py`):
   ```python
   import pytest
   from bot.plugins.start import StartPlugin
   
   @pytest.mark.asyncio
   async def test_start_plugin():
       # Mock event and bot
       pass
   ```
4. Run tests: `pytest tests/`

### Pull Request Guidelines

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes and commit: `git commit -m "Add my feature"`
4. Push to your fork: `git push origin feature/my-feature`
5. Open a Pull Request with:
   - Clear description of changes
   - Test results (if applicable)
   - Screenshots for UI changes

## Deployment Notes

- **Session File**: `telethon_bot.session` is auto-generated on first run. Keep it secure—it contains authentication data.
- **Environment Variables**: Never commit `.env` to version control. Use `.gitignore`.
- **Logging**: In production, consider log rotation (e.g., using `logrotate` on Linux) to prevent `bot.log` from growing too large.
- **Monitoring**: Use tools like `systemd` status, `docker logs`, or services like Sentry for error tracking.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

**Developed by [Monsur](https://t.me/minkxx69)**  
**Repository**: [github.com/monsurcodes/telethon_bot_boilerplate](https://github.com/monsurcodes/telethon_bot_boilerplate)

For questions or issues, please open an issue on GitHub or contact the developer on Telegram.
