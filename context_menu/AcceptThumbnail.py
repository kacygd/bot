from discord import Interaction, Embed, Message
from discord.app_commands import default_permissions
from util.functions import log
#from modals.acceptThumbnail import acceptThumbnailForm
from json import load

def commandFunction(tree, client):
    @tree.context_menu(name="Accept Thumbnail")
    @default_permissions(manage_messages=True)
    async def addQuote(interaction:Interaction, message: Message):
        with open("specialConfig.json", "r") as specialConfigFile:
            specialConfig = load(specialConfigFile)
        if interaction.guild.id != specialConfig["guild"]:
            embed = Embed(title=" ",description="**:x: You cannot use this here!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to edit a message")
            return
        
        #await interaction.response.send_modal(acceptThumbnailForm(client, message))