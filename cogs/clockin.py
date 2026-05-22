import discord
from discord.ext import commands
from dotenv import load_dotenv
from decorators import role_decorators
from data.models import Session
from datetime import datetime, timezone, timedelta
import os

load_dotenv()
MANAGER_ROLE_NAME = os.getenv("MANAGER_ROLE_NAME") or "Shift manager"


class ClockView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Clock In",
        style=discord.ButtonStyle.green,
        custom_id="clock_in_btn"
    )
    async def clock_in(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        """
        Handles the "Clock In" button interaction for the Discord bot.

        The method checks if the user already has an active session (not clocked out). If an
        open session exists, it sends a response informing the user that they are already
        clocked in. Otherwise, it creates a new session entry with the current UTC timestamp
        as the clock-in time.

        :param interaction: The interaction object representing the user's interaction with
            the clock-in button.
        :type interaction: discord.Interaction
        :param button: The button object for the "Clock In" button.
        :type button: discord.ui.Button
        :return: None
        """
        user_id = str(interaction.user.id)

        open_session = await Session.filter(user_id=user_id, clock_out=None).first()
        if open_session:
            return await interaction.response.send_message(
                "Already clocked in.",
                ephemeral=True
            )

        now = datetime.now(timezone.utc)

        await Session.create(
            user_id=user_id,
            clock_in=now,
            clock_out=None
        )

        return await interaction.response.send_message(
            f"Clocked in",
            ephemeral=True
        )

    @discord.ui.button(
        label="Clock Out",
        style=discord.ButtonStyle.red,
        custom_id="clock_out_btn"
    )
    async def clock_out(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        """
        This method handles the "Clock Out" functionality when the corresponding button is pressed in the Discord UI.
        It updates the user's session to record the clock-out time if a valid clock-in session exists. If there's no
        active session or clock-in entry, a response indicating the user is not clocked in will be sent.

        :param interaction: The interaction object representing the user's interaction with the Discord bot.
            Used to extract user information and send responses.
        :type interaction: discord.Interaction

        :param button: The button object representing the "Clock Out" button in the Discord UI.
        :type button: discord.ui.Button

        :return: None. The method is asynchronous and sends a response to the Discord interaction when completed.
        """
        user_id = str(interaction.user.id)

        session = await Session.filter(user_id=user_id, clock_out=None).first()
        if not session:
            return await interaction.response.send_message(
                "Not clocked in.",
                ephemeral=True
            )

        now = datetime.now(timezone.utc)
        session.clock_out = now
        await session.save()

        duration = now - session.clock_in

        return await interaction.response.send_message(
            f"Clocked out. Worked {str(duration).split('.')[0]}",
            ephemeral=True
        )


def _start_of_year(now: datetime) -> datetime:
    return now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)


def _start_of_month(now: datetime) -> datetime:
    return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def _start_of_week(now: datetime) -> datetime:
    # Monday = 0
    start = now - timedelta(days=now.weekday())
    return start.replace(hour=0, minute=0, second=0, microsecond=0)


def _start_of_day(now: datetime) -> datetime:
    return now.replace(hour=0, minute=0, second=0, microsecond=0)


def _sum_sessions(sessions, now: datetime) -> timedelta:
    total = timedelta()

    for s in sessions:
        start = s.clock_in
        end = s.clock_out or now
        total += (end - start)

    return total


class ClockInCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="clockin_init")
    @role_decorators.requires_role_or_admin(MANAGER_ROLE_NAME)
    async def clockin_init(self, ctx: commands.Context) -> None:
        """Create the clock-in panel"""

        view = ClockView()

        await ctx.send(
            "🕒 **Clock In System**\nUse the buttons below:",
            view=view
        )

    @commands.hybrid_command(name="work_stats")
    async def work_stats(self, ctx: commands.Context, member: discord.Member | None = None, public: bool = False) -> None:
        """
        Provides the work statistics for a Discord member, such as the total work duration
        for the current day, week, month, and year. The command can be invoked to view
        the stats for the invoking user or another member, if the invoker has the
        necessary permissions.

        :param ctx: The invocation context of the command.
        :type ctx: commands.Context
        :param member: The Discord member for whom the work stats are being requested.
                       Defaults to the invoking user.
                       Required permissions apply if the `member` is not the invoking user.
        :type member: discord.Member | None
        :param public: A flag indicating whether the response should be visible to others
                       in the channel. Defaults to False (making the response ephemeral).
        :type public: bool
        :return: None.
        :rtype: None
        """
        member = member or ctx.author
        role = discord.utils.find(lambda r: r.name == MANAGER_ROLE_NAME, ctx.guild.roles)

        is_manager = role in ctx.author.roles
        is_admin = ctx.author.guild_permissions.administrator

        if member != ctx.author and not (is_admin or is_manager):
            await ctx.reply(
                "Only managers and administrators can view other members' work stats.",
                ephemeral=True
            )
            return

        user_id = str(member.id)
        now = datetime.now(timezone.utc)

        start_day = _start_of_day(now)
        start_week = _start_of_week(now)
        start_month = _start_of_month(now)
        start_year = _start_of_year(now)

        day_sessions = await Session.filter(user_id=user_id, clock_in__gte=start_day)
        week_sessions = await Session.filter(user_id=user_id, clock_in__gte=start_week)
        month_sessions = await Session.filter(user_id=user_id, clock_in__gte=start_month)
        year_sessions = await Session.filter(user_id=user_id, clock_in__gte=start_year)

        day_total = _sum_sessions(day_sessions, now)
        week_total = _sum_sessions(week_sessions, now)
        month_total = _sum_sessions(month_sessions, now)
        year_total = _sum_sessions(year_sessions, now)

        def fmt(td: timedelta):
            seconds = int(td.total_seconds())
            h = seconds // 3600
            m = (seconds % 3600) // 60
            return f"{h}h {m}m"

        embed = discord.Embed(
            title=f"Work stats for {member.display_name}",
            color=discord.Color.blurple(),
        )

        embed.add_field(name="Today", value=fmt(day_total), inline=False)
        embed.add_field(name="This week", value=fmt(week_total), inline=False)
        embed.add_field(name="This month", value=fmt(month_total), inline=False)
        embed.add_field(name="This year", value=fmt(year_total), inline=False)

        await ctx.reply(embed=embed, ephemeral=not public)

    @commands.Cog.listener()
    async def on_ready(self):
        ...


async def setup(bot: commands.Bot):
    await bot.add_cog(ClockInCog(bot))
    bot.add_view(ClockView())
