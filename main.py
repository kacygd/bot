from discord import Client, Intents, ActivityType, Activity
from discord.app_commands import CommandTree
from util.resources import TOKEN
from util.functions import log 
from os import listdir, remove
from os.path import isfile, join, getmtime, splitext
from discord.ext import tasks
from datetime import datetime, timedelta
from json import dump, load

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
        print(f"Logged in as {self.user}.")
        await client.change_presence(activity=Activity(type=ActivityType.playing, name="PlusGDPS"))
        log(f"(SUCCESS) {self.user} has been STARTED. Ping: {round (client.latency * 1000)} ms")
        await thumbnails_delete_and_poll_lock.start()
        
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
async def thumbnails_delete_and_poll_lock():
    try:
        await bg_task()
    except:
        log("(ERROR) An error occurred in task loop")
async def bg_task():
    changed = False
    with open("data/threads.json", "r") as file:
        try:
            threads = load(file)["threads"]
            max = len(threads)
            i = 0
            now = int(datetime.now().timestamp())
        except:
            log("(ERROR) Error when initializing threads data")
            return
        while(i < max):
            try:
                thread = threads[i]
                if (not "time" in thread.keys()) or thread["time"] <= now:
                    threads.remove(thread)
                    changed = True
                    max -= 1
                    try:
                        await client.get_channel(thread["channel"]).get_thread(thread["thread"]).edit(locked=True)
                    except:
                        log(f"(ERROR) Unable to lock thread {thread["thread"]} in channel {thread["channel"]}")
                i += 1
            except:
                log(f"(ERROR) Error in thread #{i}      ({threads})")
    if changed:
        with open("data/threads.json", "w") as file:
            dump({"threads":threads}, file)
    with open("thumbnails.json", "r") as thumbnailsFile:
        thumbnailsData = load(thumbnailsFile)
        thumbnails = thumbnailsData.get("thumbnails", [])
    file_array = listdir("thumbnails")
    for file in file_array:
        file_path = f"thumbnails/{file}"
        base, extension = splitext(file)
        last_created = datetime.fromtimestamp(getmtime(file_path))
        difference = datetime.now() - last_created
        if difference > timedelta(days=1):
            remove(file_path)
            thumbnails.remove(int(base))
            json_dict = {"thumbnails": thumbnails}
            with open("thumbnails.json", "w") as thumbnailsFile:
                dump(json_dict, thumbnailsFile, indent=4)

            log(f"(CLEANUP) DELETED thumbnail '{base}'")
            
client.run(TOKEN)