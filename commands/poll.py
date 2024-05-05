from discord import Interaction, Role, Embed, TextChannel
from discord.app_commands import default_permissions, Group
from json import load, dump
from util.functions import log
from util.translate import translate, get_language
from modals.poll import pollModal

def commandFunction(tree, client):
    group = Group(name="poll",description="Manage and send polls")
    @group.command(name="send",description="Send a poll")
    async def send(interaction:Interaction, question:str, multiselect:bool, hours:int = 1):
        lang = get_language(interaction.user.id, interaction.locale.name)
        with open("specialConfig.json", "r") as specialConfigFile:
            data = load(specialConfigFile)
            server = data["server"]
            pollChannel = data["pollChannel"]
            pollRole = data["pollRole"]
        if interaction.guild.id != server:
            embed = Embed(title=" ",description=f"**:x: {translate('cmd.error.not_here', lang)}**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to send a poll (not allowed)")
            return
        if pollChannel == 0 or pollRole == 0:
            embed = Embed(title=" ",description=f"**:x: {translate('cmd.error.config', lang)}**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to send a poll (not configured)")
            return
        if interaction.user.get_role(pollRole) == None:
            embed = Embed(title=" ",description=f"**:x: {translate('error.no_permission', lang)}**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to send a poll (not allowed)")
            return
        if len(question) > 45:
            embed = Embed(title=" ",description=f"**:x: {translate('cmd.error.invalid', lang)}**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to send a poll (too long question)")
            return
        if hours > 168 or hours <= 0:
            embed = Embed(title=" ",description=f"**:x: {translate('cmd.error.invalid', lang)}**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to send a poll (invalid duration)")
            return
        await interaction.response.send_modal(pollModal(question, multiselect, lang, pollChannel, hours, client))

    @group.command(name="role",description="Edit poll create role")
    @default_permissions(administrator=True)
    async def role(interaction:Interaction, role:Role):
        with open("specialConfig.json", "r") as specialConfigFile:
            lang = get_language(interaction.user.id, interaction.locale.name)
            data = load(specialConfigFile)
            server = data["server"]
            pollRole = data["pollRole"]
        
            if interaction.guild.id != server:
                embed = Embed(title=" ",description=f"**:x: {translate('cmd.error.not_here', lang)}**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the poll role (not allowed)")
                return
        
            if role.id == pollRole:
                embed = Embed(title=" ",description=f"**:x: {translate('cmd.error.role.same', lang)}**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the poll role (same role)")
                return
            
            else:
                data["pollRole"] = role.id
                try:
                    with open("specialConfig.json", "w") as specialConfigFile:
                        dump(data, specialConfigFile, indent=4)
                    embed = Embed(title=" ",description=f"**:white_check_mark: {translate('cmd.poll_role.success', lang)}** <@&{role.id}>**!**",colour=2067276)
                    await interaction.response.send_message(" ",embed=embed)
                    log(f"(SUCCESS) Poll role has been CHANGED")
                except:
                    embed = Embed(title=" ",description=f"**:x: {translate('error.generic', lang)}**",colour=15548997)
                    await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                    log(f"(FAILED) {interaction.user} FAILED to change the poll role (error when writing in specialConfig.json/when sending the success embed)")
    @group.command(name="channel",description="Edit poll channel")
    @default_permissions(administrator=True)
    async def channel(interaction:Interaction, channel:TextChannel):
        with open("specialConfig.json", "r") as specialConfigFile:
            data = load(specialConfigFile)
            server = data["server"]
            pollChannel = data["pollChannel"]
            lang = get_language(interaction.user.id, interaction.locale.name)
        
            if interaction.guild.id != server:
                embed = Embed(title=" ",description=f"**:x: {translate('cmd.error.not_here', lang)}**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the poll channel (not allowed)")
                return
            if channel.id == pollChannel:
                embed = Embed(title=" ",description=f"**:x: {translate('cmd.error.channel.same', lang)}**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the poll channel (already set)")
                return
            else:
                data["pollChannel"] = channel.id
                try:
                    with open("specialConfig.json", "w") as specialConfigFile:
                        dump(data, specialConfigFile, indent=4)
                    embed = Embed(title=" ",description=f"**:white_check_mark: {translate('cmd.poll_channel.success', lang)}** <#{pollChannel}>!",colour=2067276)
                    await interaction.response.send_message(" ",embed=embed)
                    log(f"(SUCCESS) Poll Channel has been CHANGED")
                except:
                    embed = Embed(title=" ",description=f"**:x: {translate('error.generic', lang)}**",colour=15548997)
                    await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                    log(f"(FAILED) {interaction.user} FAILED to change the poll channel (error when writing in specialConfig.json/when sending the success embed)")
    tree.add_command(group)