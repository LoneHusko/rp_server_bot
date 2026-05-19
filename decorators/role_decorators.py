from discord.ext import commands
import discord


def requires_role_or_admin(role_name: str):
    async def predicate(ctx: commands.Context):
        guild = ctx.guild
        if guild is None:
            await ctx.interaction.response.send_message(
                f"This command can only be used in a server.",
                ephemeral=True
            )
            return False
        user = ctx.author
        if user is None:
            await ctx.interaction.response.send_message(
                f"This command can only be used in a server.",
                ephemeral=True
            )
            return False

        role = discord.utils.find(lambda r: r.name == role_name, guild.roles)

        if user.guild_permissions.administrator:
            return True

        if role is None:
            if ctx.interaction:
                await ctx.interaction.response.send_message(
                    f"The **{role_name}** role does not exist. Only an administrator can use this command.",
                    ephemeral=True
                )
            else:
                await ctx.send(
                    f"The **{role_name}** role does not exist. Only an administrator can use this command."
                )
            return False

        if role not in user.roles:
            if ctx.interaction:
                await ctx.interaction.response.send_message(
                    f"You must have the **{role_name}** role to use this command.",
                    ephemeral=True
                )
            else:
                await ctx.send(
                    f"You must have the **{role_name}** role to use this command."
                )
            return False

        return True

    return commands.check(predicate)
