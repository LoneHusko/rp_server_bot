import tortoise
import discord
import os
import dotenv
from discord.ext import commands

dotenv.load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
REQUIRED_PERMISSIONS = discord.Permissions(
    send_messages=True,
    manage_roles=True,
    view_channel=True,
    use_application_commands=True,
)
GUILD_ID = int(os.getenv("GUILD_ID", 0))
if GUILD_ID == 0:
    raise RuntimeError("GUILD_ID is not set")


intents = discord.Intents.default()
# noinspection PyDunderSlots,PyUnresolvedReferences
intents.members = True

client = commands.Bot(intents=intents, command_prefix="!")


async def init_db():
    if not os.path.exists("db"):
        os.mkdir("db")
    await tortoise.Tortoise.init(
        db_url="sqlite://db/database.db",
        modules={"models": ["data.models"]},
    )
    await tortoise.Tortoise.generate_schemas()


async def load_cogs() -> None:
    """
    Load and initialize all cog extensions in the cogs directory asynchronously.

    :return: None
    """
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await client.load_extension(f'cogs.{filename[:-3]}')
            except Exception as e:
                print(f'Failed to load cog {filename}: {e}')


@client.event
async def on_ready() -> None:
    """
    Handles the bot's login and initialization process after establishing a connection to Discord.

    Verifies the bot's presence in the correct guild, ensures the bot is not a member of multiple guilds,
    retrieves the bot's user and member data, checks for required permissions in the guild, and loads the
    necessary cogs for the bot's functionality.

    :raises RuntimeError:
        If the bot is not a member of the specified guild.
        If the bot is a member of multiple guilds at once.
        If the bot user information is unavailable.
        If the permissions required to function in the guild are not granted to the bot.

    :return: None
    """
    guild = client.get_guild(GUILD_ID)

    if guild is None:
        raise RuntimeError("Bot is not in the target guild.")

    if len(client.guilds) > 1:
        raise RuntimeError("Bot is in multiple guilds.")

    user = client.user
    if user is None:
        raise RuntimeError("Bot user is not available.")

    me = guild.get_member(user.id)

    if me is None:
        me = await guild.fetch_member(user.id)

    if not me.guild_permissions >= REQUIRED_PERMISSIONS:
        raise RuntimeError("Missing permissions. Please grant the bot the following permissions:\n - Send messages\n - Manage roles\n - View channel\n - Use application commands")

    await load_cogs()

    await client.tree.sync()
    await init_db()
    print("Bot is online")


if __name__ == "__main__":
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")
    else:
        client.run(BOT_TOKEN)
