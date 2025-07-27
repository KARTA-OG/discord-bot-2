import discord
from discord.ext import commands
from discord import app_commands
import os

class ReloadCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="reload", description="Reload all bot modules")
    @app_commands.checks.has_permissions(administrator=True)
    async def reload(self, interaction: discord.Interaction):
        reloaded = []
        failed = []

        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                ext = f"cogs.{filename[:-3]}"
                try:
                    self.bot.unload_extension(ext)
                    self.bot.load_extension(ext)
                    reloaded.append(filename)
                except Exception as e:
                    failed.append((filename, str(e)))

        embed = discord.Embed(title="🔁 Reload Results", color=discord.Color.green())
        if reloaded:
            embed.add_field(name="✅ Reloaded", value="\n".join(reloaded), inline=False)
        if failed:
            embed.add_field(name="❌ Failed", value="\n".join(f"{f}: {err}" for f, err in failed), inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @reload.error
    async def reload_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ You need Administrator permissions to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"⚠️ Unexpected error: `{error}`", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ReloadCog(bot))
