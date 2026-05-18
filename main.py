import discord
import os
import dotenv

dotenv.load_dotenv()

intents = discord.Intents.default()

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

BOT_TOKEN = os.getenv("TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")
else:
    client.run(BOT_TOKEN)
