import discord
from discord.ext import commands
import os
import json
from keep_alive import keep_alive  # 🔁 Render ping system

# Start keep-alive server before bot starts
keep_alive()

# Enable necessary intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.members = True

# Load config file
with open("config.json") as f:
    config = json.load(f)

# Create the bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user.name}")
    print("🔁 Bot is ready!")

@bot.event
async def setup_hook():
    # Slash command sync to test server or global
    if config.get("test_guild_id"):
        test_guild = discord.Object(id=int(config["test_guild_id"]))
        await bot.tree.sync(guild=test_guild)
        print(f"🧪 Slash commands synced to test server: {config['test_guild_id']}")
    else:
        await bot.tree.sync()
        print("🌐 Slash commands synced globally")

# Load all cogs from the cogs/ folder
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        print(f"✅ Loaded extension: {filename}")

# Run the bot using the TOKEN from Render environment
bot.run(os.environ["TOKEN"])
