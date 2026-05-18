
# RP Server Bot

A Discord bot for providing basic functionalities for an RP server. The bot currently verifies that it is running in the configured Discord server, checks that it has the required permissions, loads cog extensions, and automatically assigns a default role to new members when they join.

## Features

- Connects to a single configured Discord guild
- Validates required bot permissions on startup
- Loads extensions from the `cogs` directory
- Assigns a default role to new members
- Uses environment variables for configuration

## Requirements

- Python 3.10 or newer recommended
- A Discord bot application
- `discord.py`
- `python-dotenv`

Install all Python dependencies with:
```cmd
pip install -r requirements.txt
```
## Project Structure
```text
rp_server_bot/
├── cogs/
│   └── members.py
├── ENV_VARIABLES
├── LICENSE
├── main.py
├── README.md
└── requirements.txt
```
## Environment Variables

The bot requires the following environment variables:

| Variable | Description |
| --- | --- |
| `BOT_TOKEN` | Your Discord bot token |
| `GUILD_ID` | The ID of the Discord server the bot should run in |
| `DEFAULT_ROLE_ID` | The ID of the role assigned to new members |

Create a `.env` file in the project root:
```env
BOT_TOKEN=your_bot_token_here
GUILD_ID=your_guild_id_here
DEFAULT_ROLE_ID=your_default_role_id_here
```
Do **not** commit your `.env` file or bot token to version control.

## Discord Bot Setup

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create or select your application.
3. Open the **Bot** section.
4. Copy the bot token and use it as `BOT_TOKEN`.
5. Enable the required privileged intent:
   - **Server Members Intent**
6. Invite the bot to your server with the required permissions.

## Required Bot Permissions

The bot checks for the following permissions:

- Send Messages
- Manage Roles
- View Channels
- Use Application Commands

The bot also needs its highest role to be above the default role it assigns to new members.

## Getting IDs from Discord

To copy server and role IDs:

1. Open Discord.
2. Go to **User Settings → Advanced**.
3. Enable **Developer Mode**.
4. Right-click your server and choose **Copy Server ID**.
5. Right-click the role and choose **Copy Role ID**.

## Running the Bot

After installing dependencies and creating your `.env` file, run:
```cmd
python main.py
```
If everything is configured correctly, the bot will start and print:
```text
Bot is online
```
## Cogs

Bot functionality is organized into cogs.

The current cog is:

- `members.py` — handles member join events and assigns the configured default role.

Additional `.py` files placed in the `cogs` directory can be loaded automatically by the bot.

## Troubleshooting

### `BOT_TOKEN is not set`

Make sure your `.env` file contains:
```
env
BOT_TOKEN=your_bot_token_here
```
### `GUILD_ID is not set`

Make sure `GUILD_ID` is set to your Discord server ID.

### `DEFAULT_ROLE_ID is not set`

Make sure `DEFAULT_ROLE_ID` is set to the ID of the role you want new members to receive.

### `Missing permissions`

Make sure the bot has the required permissions in your server.

### New members are not receiving the default role

Check that:

- **Server Members Intent** is enabled in the Discord Developer Portal
- The bot has the **Manage Roles** permission
- The bot's highest role is above the default role
- `DEFAULT_ROLE_ID` is correct

## License

See the `LICENSE` file for license information.

