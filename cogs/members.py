import os
import discord
import dotenv
from discord.ext import commands

dotenv.load_dotenv()
GUILD_ID = int(os.getenv("GUILD_ID", 0))
if GUILD_ID == 0:
    raise RuntimeError("GUILD_ID is not set")
DEFAULT_ROLE_ID = int(os.getenv("DEFAULT_ROLE_ID", 0))
if DEFAULT_ROLE_ID == 0:
    raise RuntimeError("DEFAULT_ROLE_ID is not set")


class MembersCog(commands.Cog):
    """
    Handles all member-related events and commands
    """

    def __init__(self, bot: discord.ext.commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        """
        Event listener for when a member joins a Discord server.

        This function listens for the `on_member_join` event, which is triggered when a member joins
        the server. It assigns a default role to the newly joined member.

        :param member: The `discord.Member` object representing the member who joined the server.
        :type member: discord.Member
        :raises RuntimeError: If the bot is not in the target guild or the default role cannot be found.
        :return: None
        """
        guild = self.bot.get_guild(GUILD_ID)
        if guild is None:
            print("Bot is not in the target guild")
            return
        role = guild.get_role(DEFAULT_ROLE_ID)
        if role is None:
            print("Default role is not found on this guild")
            return
        await member.add_roles(role)


async def setup(bot) -> None:
    """
    Load the "members" cog
    """

    await bot.add_cog(MembersCog(bot))
