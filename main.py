import discord
from discord.ext import commands
import os
import json
from keep_alive import keep_alive

# 🔁 Start keep-alive server for Render
keep_alive()

# 🔧 Enable required intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.members = True

# 📦 Load config.json
with open("config.json") as f:
    config = json.load(f)

# 🚀 Create bot
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user.name}")
    print("🔁 Bot is ready!")

@bot.event
async def setup_hook():
    print("🧪 Syncing slash commands and loading cogs...")

    # 🔄 Load all cogs
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Loaded extension: {filename}")
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")

    # 🧪 Sync slash commands to test server
    try:
        if config.get("test_guild_id"):
            test_guild = discord.Object(id=int(config["test_guild_id"]))
            await bot.tree.sync(guild=test_guild)
            print(f"✅ Slash commands synced to test server: {config['test_guild_id']}")
        else:
            print("⚠️ No test_guild_id provided.")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

# 🔑 Start the bot
bot.run(os.environ["TOKEN"])
