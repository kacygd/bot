from discord import Interaction, Embed, Role
from discord.app_commands import default_permissions
from util.functions import log
from json import load, dump
from util.translate import get_language, translate

def commandFunction(tree, client):
    @tree.command(name="thumbnail_role",description="Change the thumbnail role")
    @default_permissions(administrator=True)
    async def thumbnailRoleCommand(interaction: Interaction, role: Role):
        with open("specialConfig.json", "r") as specialConfigFile:
            lang = get_language(interaction.user.id, interaction.locale.name)
            data = load(specialConfigFile)
            server = data["server"]
            verifiedThumbnailerRole = data["verifiedThumbnailerRole"]
        
            if interaction.guild.id != server:
                embed = Embed(title=" ",description=f"**:x: {translate('cmd.error.not_here', lang)}**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the verified thumbnailer role (not allowed)")
                return
        
            if role.id == verifiedThumbnailerRole:
                embed = Embed(title=" ",description=f"**:x: {translate('cmd.error.role.same', lang)}**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the verified thumbnailer role (same role)")
                return
            
            else:
                data["verifiedThumbnailerRole"] = role.id

                try:
                    with open("specialConfig.json", "w") as specialConfigFile:
                        dump(data, specialConfigFile, indent=4)
                    embed = Embed(title=" ",description=f"**:white_check_mark: {translate('cmd.thumb_role.success', lang)}** <@&{role.id}>**!**",colour=2067276)
                    await interaction.response.send_message(" ",embed=embed)
                    log(f"(SUCCESS) Verified thumbnailer role has been CHANGED")
                except:
                    embed = Embed(title=" ",description=f"**:x: {translate('error.generic', lang)}**",colour=15548997)
                    await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                    log(f"(FAILED) {interaction.user} FAILED to change the verified thumbnailer role (error when writing in specialConfig.json/when sending the success embed)")