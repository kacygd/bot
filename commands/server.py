from discord import Interaction, Embed
from discord.app_commands import default_permissions
from util.functions import log
from json import load, dump
from util.translate import get_language, translate

def commandFunction(tree, client):
    @tree.command(name="server",description="Change the server where the bot should be used")
    @default_permissions(administrator=True)
    async def serverCommand(interaction: Interaction):
        with open("specialConfig.json", "r") as specialConfigFile:
            data = load(specialConfigFile)
            server = data["server"]
        lang = get_language(interaction.user.id)
        if interaction.user.id != 629711559899217950:
            translation:str = translate("error.no_permission", lang)
            embed = Embed(title=" ",description=f"**:x: {translation}**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to change the server (not allowed)")
            return
        
        if interaction.guild.id == server:
            translation:str = translate("cmd.error.server.same", lang)
            embed = Embed(title=" ",description=f"**:x: {translation}**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to change the server (same server)")
            return
            
        else:
            data["server"] = interaction.guild.id

            try:
                with open("specialConfig.json", "w") as specialConfigFile:
                    dump(data, specialConfigFile, indent=4)
                translation:str = translate("cmd.server.success", lang)
                embed = Embed(title=" ",description=f"**:white_check_mark: {translate}** ``{interaction.guild}``!",colour=2067276)
                await interaction.response.send_message(" ",embed=embed)
                log(f"(SUCCESS) Server has been CHANGED")
            except:
                translation:str = translate("error.generic", lang)
                embed = Embed(title=" ",description=f"**:x: {translation}**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the server (error when writing in specialConfig.json/when sending the success embed)")