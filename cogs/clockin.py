import discord
from discord.ext import commands


class ClockView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Clock In",
        style=discord.ButtonStyle.green,
        custom_id="clock_in_btn"
    )
    async def clock_in(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            f"Clocked in",
            ephemeral=True
        )

    @discord.ui.button(
        label="Clock Out",
        style=discord.ButtonStyle.red,
        custom_id="clock_out_btn"
    )
    async def clock_out(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            f"Clocked out",
            ephemeral=True
        )


class ClockInCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="clockin_init")
    async def clockin_init(self, ctx: commands.Context):
        """Create the clock-in panel"""

        view = ClockView()

        await ctx.send(
            "🕒 **Clock In System**\nUse the buttons below:",
            view=view
        )

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(ClockView())


async def setup(bot: commands.Bot):

    await bot.add_cog(ClockInCog(bot))