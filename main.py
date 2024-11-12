import disnake
from disnake.ext.commands import InteractionBot
import os
import json
with open(r'./config.json', 'r') as f:
        data = json.load(f)
intents = disnake.Intents.all()
bot = InteractionBot()




@bot.event
async def on_ready():
    
    print("Im ready")

for file in os.listdir(r"./cogs"):
    if file.endswith(".py"):
        print(file)
        bot.load_extension(f"cogs.{file[:-3]}")






bot.run(os.getenv("GIVEAWAYS_TOKEN"))