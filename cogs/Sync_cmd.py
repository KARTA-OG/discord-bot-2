from discord.ext import commands

class SyncCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sync")
    @commands.is_owner()
    async def sync(self, ctx):
        synced = await self.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"✅ Synced {len(synced)} command(s) to this server.")

async def setup(bot):
    await bot.add_cog(SyncCommand(bot))
