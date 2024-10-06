from discord import Interaction, Embed
from discord.app_commands import Group
from json import load, dump
from util.functions import log
from util.translate import translate, get_language
from os.path import exists
from time import time

def commandFunction(tree, client):
    group = Group(name="dead",description="Ping Dead Chat")
    @group.command(name="chat",description="Ping Dead Chat")
    async def chat(interaction:Interaction):
        lang = get_language(interaction.user.id, interaction.locale.name)
        with open("specialConfig.json", "r") as specialConfigFile:
            data = load(specialConfigFile)
            server = data["server"]
            deadChatAllowedRole = data["deadChatAllowedRole"]
            deadChatRole = data["deadChatRole"]
        if interaction.guild.id != server:
            embed = Embed(title=" ",description=f"**:x: {translate('cmd.error.not_here', lang)}**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to use /dead chat (not allowed)")
            return
        if deadChatAllowedRole == 0 or deadChatRole == 0:
            embed = Embed(title=" ",description=f"**:x: {translate('cmd.error.config', lang)}**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to use /poll (not configured)")
            return
        if interaction.user.get_role(deadChatAllowedRole) == None:
            embed = Embed(title=" ",description=f"**:x: {translate('error.no_permission', lang)}**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to use /dead chat (not allowed)")
            return
        
        timestamp_file = "deadchat_timestamp.json"
        current_time = time()
        time_limit = 3600 # seconds

        if exists(timestamp_file):
            with open(timestamp_file, "r") as file:
                last_ping_time = load(file).get("last_ping", 0)

            if current_time - last_ping_time < time_limit:
                embed = Embed(title=" ", description=f"**:x: {translate('cmd.error.cooldown', lang)}**", colour=15548997)
                await interaction.response.send_message(" ", embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to use /dead chat (on cooldown)")
                return

        with open(timestamp_file, "w") as file:
            dump({"last_ping": current_time}, file)

        await interaction.response.send_message(f"<@&{deadChatRole}>")
    tree.add_command(group)
