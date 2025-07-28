import discord
from discord.ext import commands
from discord import app_commands

class TestCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="test", description="Test command to check if slash commands are working.")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message("✅ Slash commands are working!")

async def setup(bot):
    await bot.add_cog(TestCommand(bot))
