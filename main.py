import discord
import os
import dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


intents = discord.Intents.default()

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")
else:
    client.run(BOT_TOKEN)
