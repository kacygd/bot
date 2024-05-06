from discord import Interaction, Role, Embed, TextChannel
from discord.app_commands import default_permissions, Group
from json import load, dump
from util.functions import log
from util.translate import translate, get_language
from modals.poll import pollModal

def commandFunction(tree, client):
    group = Group(name="poll",description="Manage and send polls")
    @group.command(name="send",description="Send a poll")
    async def send(interaction:Interaction, question:str, multiselect:bool = False, hours:int = 1):
        lang = get_language(interaction.user.id, interaction.locale.name)
        with open("specialConfig.json", "r") as specialConfigFile:
            data = load(specialConfigFile)
            server = data["server"]
            pollChannel = data["pollChannel"]
            pollMessage = data["pollMessage"]
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
        await interaction.response.send_modal(pollModal(question, multiselect, lang, pollChannel, hours, client, pollMessage, [data["placeholder1"],data["placeholder2"],data["placeholder3"],data["placeholder4"],data["placeholder5"]]))

    @group.command(name="role",description="Edit poll create role")
    async def role(interaction:Interaction, role:Role):
        lang = get_language(interaction.user.id, interaction.locale.name)
        if not interaction.user.guild_permissions.administrator:
            embed = Embed(title=" ",description=f"**:x: {translate('error.no_permission', lang)}**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to change the poll role (not allowed)")
            return
        with open("specialConfig.json", "r") as specialConfigFile:
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
    async def channel(interaction:Interaction, channel:TextChannel):
        lang = get_language(interaction.user.id, interaction.locale.name)
        if not interaction.user.guild_permissions.administrator:
            embed = Embed(title=" ",description=f"**:x: {translate('error.no_permission', lang)}**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to change the poll channel (not allowed)")
            return
        with open("specialConfig.json", "r") as specialConfigFile:
            data = load(specialConfigFile)
            server = data["server"]
            pollChannel = data["pollChannel"]
        
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
    
    @group.command(name="config",description="Edit poll config")
    async def channel(interaction:Interaction, message:str = None, placeholder1:str = None, placeholder2:str = None, placeholder3:str = None, placeholder4:str = None, placeholder5:str = None):
        lang = get_language(interaction.user.id, interaction.locale.name)
        if not interaction.user.guild_permissions.administrator:
            embed = Embed(title=" ",description=f"**:x: {translate('error.no_permission', lang)}**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to change the poll message (not allowed)")
            return
        with open("specialConfig.json", "r") as specialConfigFile:
            data = load(specialConfigFile)
            server = data["server"]
        
            if interaction.guild.id != server:
                embed = Embed(title=" ",description=f"**:x: {translate('cmd.error.not_here', lang)}**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the poll config (not allowed)")
                return
            else:
                if message != None: data["pollMessage"] = message
                if placeholder1 != None: data["placeholder1"] = placeholder1
                if placeholder2 != None: data["placeholder2"] = placeholder2
                if placeholder3 != None: data["placeholder3"] = placeholder3
                if placeholder4 != None: data["placeholder4"] = placeholder4
                if placeholder5 != None: data["placeholder5"] = placeholder5
                try:
                    with open("specialConfig.json", "w") as specialConfigFile:
                        dump(data, specialConfigFile, indent=4)
                    embed = Embed(title=" ",description=f"**:white_check_mark: {translate('cmd.poll_config.success', lang)}**",colour=2067276)
                    await interaction.response.send_message(" ",embed=embed)
                    log(f"(SUCCESS) Poll message has been CHANGED")
                except:
                    embed = Embed(title=" ",description=f"**:x: {translate('error.generic', lang)}**",colour=15548997)
                    await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                    log(f"(FAILED) {interaction.user} FAILED to change the poll config (error when writing in specialConfig.json/when sending the success embed)")
    tree.add_command(group)