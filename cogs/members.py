import discord
from discord.ext import commands


class MembersCog(commands.Cog):
    """
    Handles all member-related events and commands
    """

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        print(f"{member} has joined the server!")


async def setup(bot) -> None:
    """
    Load the "members" cog
    """

    await bot.add_cog(MembersCog(bot))
