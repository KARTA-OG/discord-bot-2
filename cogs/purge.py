import discord
from discord.ext import commands
from discord import app_commands

class PurgeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="purge", description="Delete messages in bulk (1–50)")
    @app_commands.describe(amount="Number of messages to delete (1–50)")
    @app_commands.checks.has_permissions(administrator=True)
    async def purge(self, interaction: discord.Interaction, amount: int):
        if amount < 1 or amount > 50:
            await interaction.response.send_message("❌ You can only delete between 1 and 50 messages.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True, thinking=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"🧹 Deleted {len(deleted)} messages.", ephemeral=True)

    @purge.error
    async def purge_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ You need Administrator permissions to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"⚠️ Unexpected error: `{error}`", ephemeral=True)

async def setup(bot):
    await bot.add_cog(PurgeCommand(bot))
