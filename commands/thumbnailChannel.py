from discord import Interaction, Embed, TextChannel, Thread
from discord.app_commands import default_permissions
from util.functions import log
from json import load, dump

def commandFunction(tree, client):
    @tree.command(name="thumbnail_channel",description="Change the thumbnail channel")
    @default_permissions(administrator=True)
    async def thumbnailCommand(interaction: Interaction, channel: TextChannel = None, thread: Thread = None):
        with open("specialConfig.json", "r") as specialConfigFile:
            data = load(specialConfigFile)
            server = data["server"]
            thumbnailChannel = data["thumbnailsChannel"]
        
            if interaction.guild.id != server:
                embed = Embed(title=" ",description="**:x: You are not allowed to use this here!**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the database URL (not allowed)")
                return
            
            if channel is None and thread is None:
                embed = Embed(title=" ",description="**:x: Please select atleast one channel!**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the thumbnail channel (no channels selected)")
                return

            if (channel is not None and channel.id == thumbnailChannel) or (thread is not None and thread.id == thumbnailChannel):
                embed = Embed(title=" ",description="**:x: This channel is already set!**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the thumbnail channel (already set)")
                return
            
            if channel is not None and thread is not None:
                embed = Embed(title=" ",description="**:x: Please only select select channel!**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the thumbnail channel (two channels)")
                return
            
            else:
                if channel != None:
                    channelId = channel.id
                if thread != None:
                    channelId = thread.id
                data["thumbnailsChannel"] = channelId

                try:
                    with open("specialConfig.json", "w") as specialConfigFile:
                        dump(data, specialConfigFile, indent=4)
                    embed = Embed(title=" ",description=f"**:white_check_mark: Successfully set the new thumbnail channel to** <#{thumbnailChannel}>!",colour=2067276)
                    await interaction.response.send_message(" ",embed=embed)
                    log(f"(SUCCESS) Thumbnail Channel has been CHANGED")
                except:
                    embed = Embed(title=" ",description="**:x: An error has occured while trying to set the new thumbnail channel**",colour=15548997)
                    await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                    log(f"(FAILED) {interaction.user} FAILED to change the thumbnail channel (error when writing in specialConfig.json/when sending the success embed)")