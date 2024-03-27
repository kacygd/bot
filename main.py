from discord import Client, Intents, ActivityType, Embed, Activity
from discord.app_commands import CommandTree
from util.resources import TOKEN
from util.functions import log 
from os import listdir, remove
from os.path import isfile, join, getmtime
from discord.ext import tasks
from random import choice
from json import load, dump
from datetime import datetime, timedelta

class aclient(Client):
    def __init__(self):
        super().__init__(intents=Intents.default())
        self.synced = False
        self.commands = {}
        self.context_menus = {}
    
    async def on_ready(self):
        if not self.synced:
            await tree.sync()
            self.synced = True
        await thumbnails_delete.start()
        print(f"Logged in as {self.user}.")
        await client.change_presence(activity=Activity(type=ActivityType.playing, name="PlusGDPS"))
        log(f"(SUCCESS) {self.user} has been STARTED. Ping: {round (client.latency * 1000)} ms")
        

client = aclient()
tree = CommandTree(client)

for command in listdir("commands"):
    if (not(isfile(join("commands", command)))):
        continue

    module = __import__("commands." + command[:-3], fromlist=["commandFunction"])
    commandObject = client.commands[command] = globals()[module.__name__] = module
    commandObject.commandFunction(tree, client)

for command in listdir("context_menu"):
    if (not(isfile(join("context_menu", command)))):
        continue
            
    module = __import__("context_menu." + command[:-3], fromlist=["commandFunction"])  # Remove the .py extension
    commandObject = client.context_menus[command] = globals()[module.__name__] = module
    commandObject.commandFunction(tree, client)

@tasks.loop(minutes=1)
async def thumbnails_delete():
    file_array = listdir("thumbnails")
    for file in file_array:
        file_path = f"thumbnails/{file}"
        last_created = datetime.fromtimestamp(getmtime(file_path))
        difference = datetime.now() - last_created
        if difference > timedelta(day=1):
            log(f"(CLEANUP) DELETED thumbnail #{file_path}")
            remove(file_path)
            
client.run(TOKEN)