from discord import Interaction, Embed
from discord.app_commands import default_permissions
from util.functions import log
from json import load, dump
from util.translate import get_language, translate

def commandFunction(tree, client):
    @tree.command(name="database",description="Change the database url of PlusGDPS (e.g.: https://gmd.pluscraft.fr/database)")
    @default_permissions(administrator=True)
    async def databaseCommand(interaction: Interaction, url: str):
        with open("specialConfig.json", "r") as specialConfigFile:
            data = load(specialConfigFile)
            server = data["server"]
            databaseUrl = data["databaseUrl"]
            lang = get_language(interaction.user.id, interaction.locale.name)

            if interaction.user.id != 629711559899217950:
                embed = Embed(title=" ",description=f"**:x: {translate('error.no_permission', lang)}**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the database URL (not allowed)")
                return
        
            if interaction.guild.id != server:
                embed = Embed(title=" ",description=f"**:x:{translate('cmd.error.not_here', lang)}**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the database URL (not allowed)")
                return
            
            if not (url.startswith("https://") or url.startswith("http://")):
                embed = Embed(title=" ",description=f"**:x: {translate('error.url.invalid', lang)}**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the database URL (invalid URL)")
                return

            if databaseUrl == url:
                embed = Embed(title=" ",description=f"**:x: {translate('cmd.error.url.same', lang)}**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the database URL (same URL)")
                return
            
            else:
                data["databaseUrl"] = url

                try:
                    with open("specialConfig.json", "w") as specialConfigFile:
                        dump(data, specialConfigFile, indent=4)
                    embed = Embed(title=" ",description=f"**:white_check_mark: {translate('cmd.data_url.success', lang)}** ``{url}``!",colour=2067276)
                    await interaction.response.send_message(" ",embed=embed)
                    log(f"(SUCCESS) Database URL has been CHANGED")
                except:
                    embed = Embed(title=" ",description=f"**:x: {translate('error.generic', lang)}**",colour=15548997)
                    await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                    log(f"(FAILED) {interaction.user} FAILED to change the database URL (error when writing in specialConfig.json/when sending the success embed)")