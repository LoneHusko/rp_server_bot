import os
import discord
import dotenv
from discord.ext import commands
from tortoise import Tortoise

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
# noinspection PyDunderSlots
intents.message_content = True


async def init_db():
    if not os.path.exists("db"):
        os.mkdir("db")

    if not Tortoise._inited:
        await Tortoise.init(
            db_url="sqlite://db/database.db",
            modules={"models": ["data.models"]},
            timezone="UTC",
        )
        await Tortoise.generate_schemas()


async def load_cogs(bot: commands.Bot) -> None:
    """
    Load and initialize all cog extensions in the cogs directory asynchronously.

    :return: None
    """
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
            except Exception as e:
                print(f"Failed to load cog {filename}: {e}")


class RPServerBot(commands.Bot):
    async def setup_hook(self) -> None:
        await init_db()
        await load_cogs(self)
        await self.tree.sync()

    async def close(self) -> None:
        await Tortoise.close_connections()
        await super().close()


client = RPServerBot(intents=intents, command_prefix="!")


@client.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError) -> None:
    if isinstance(error, commands.CheckFailure):
        return

    raise error


@client.event
async def on_ready() -> None:
    """
    Handles the bot's login checks after establishing a connection to Discord.
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
        raise RuntimeError(
            "Missing permissions. Please grant the bot the following permissions:\n"
            " - Send messages\n"
            " - Manage roles\n"
            " - View channel\n"
            " - Use application commands"
        )

    print("Bot is online")


if __name__ == "__main__":
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")
    else:
        client.run(BOT_TOKEN)
