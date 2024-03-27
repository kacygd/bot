from discord import Interaction, Embed
from discord.app_commands import default_permissions
from util.functions import log
from json import load, dump

def commandFunction(tree, client):
    @tree.command(name="database",description="Change the database url of PlusGDPS (e.g.: https://gmd.pluscraft.fr/database)")
    @default_permissions(administrator=True)
    async def databaseCommand(interaction: Interaction, url: str):
        with open("specialConfig.json", "r") as specialConfigFile:
            data = load(specialConfigFile)
            server = data["server"]
            databaseUrl = data["databaseUrl"]

            if interaction.user.id != 629711559899217950:
                embed = Embed(title=" ",description="**:x: You are not allowed to use this!**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the database URL (not allowed)")
                return
        
            if interaction.guild.id != server:
                embed = Embed(title=" ",description="**:x: You are not allowed to use this here!**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the database URL (not allowed)")
                return
            
            if "https://" not in url and "http://" not in url:
                embed = Embed(title=" ",description="**:x: Invalid URL!**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the database URL (invalid URL)")
                return

            if databaseUrl == url:
                embed = Embed(title=" ",description="**:x: This is the same URL!**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the database URL (same URL)")
                return
            
            else:
                data["databaseUrl"] = url

                try:
                    with open("specialConfig.json", "w") as specialConfigFile:
                        dump(data, specialConfigFile, indent=4)
                    embed = Embed(title=" ",description=f"**:white_check_mark: Successfully set the new database URL to** ``{url}``!",colour=2067276)
                    await interaction.response.send_message(" ",embed=embed)
                    log(f"(SUCCESS) Database URL has been CHANGED")
                except:
                    embed = Embed(title=" ",description="**:x: An error has occured while trying to set the new database URL**",colour=15548997)
                    await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                    log(f"(FAILED) {interaction.user} FAILED to change the database URL (error when writing in specialConfig.json/when sending the success embed)")