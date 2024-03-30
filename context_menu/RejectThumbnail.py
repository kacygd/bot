from discord import Interaction, Embed, Message
from util.functions import log
from modals.rejectThumbnail import rejectThumbnailForm
from json import load
from os import listdir

def commandFunction(tree, client):
    @tree.context_menu(name="Reject Thumbnail")
    async def rejectThumbnail(interaction:Interaction, message: Message):
        with open("specialConfig.json", "r") as specialConfigFile:
            specialConfig = load(specialConfigFile)
        with open("thumbnails.json", "r") as thumbnailsFile:
            thumbnailsData = load(thumbnailsFile)
            thumbnails = thumbnailsData.get("thumbnails", [])

        files = listdir("thumbnails")

        message = await interaction.channel.fetch_message(message.id)
        member = await interaction.guild.fetch_member(interaction.user.id)
        old_embed = message.embeds[0]

        if interaction.guild.id != specialConfig["server"]:
            embed = Embed(title=" ",description="**:x: You cannot use this here!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to reject a thumbnail (not allowed)")
            return
        
        if not any(role.id == specialConfig["verifiedThumbnailerRole"] for role in member.roles):
            embed = Embed(title=" ",description="**:x: You cannot use this!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to reject a thumbnail (not allowed)")
            return
        
        if message.author.id != client.user.id:
            embed = Embed(title=" ",description="**:x: This is not a message sent by the bot!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to reject a thumbnail (wrong message)")
            return
        
        if not old_embed.title[old_embed.title.rfind('(')+1:old_embed.title.rfind(')')].isdigit():
            embed = Embed(title=" ",description="**:x: Invalid message!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to accept a thumbnail (invalid message)")
            return
        
        if not old_embed.description[old_embed.description.rfind('(')+1:old_embed.description.rfind(')')].isdigit():
            embed = Embed(title=" ",description="**:x: Invalid message!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to reject a thumbnail (invalid message)")
            return

        if message.author.id != client.user.id:
            embed = Embed(title=" ",description="**:x: This is not a message sent by the bot!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to reject a thumbnail (wrong message)")
            return
        
        if str(old_embed.color) == "#ed4245":
            embed = Embed(title=" ",description="**:x: This submission has already been rejected!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to reject a thumbnail (already rejected)")
            return

        if str(old_embed.color) == "#1f8b4c":
            embed = Embed(title=" ",description="**:x: This submission has already been accepted!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to reject a thumbnail (already accepted)")
            return

        if int(old_embed.title[old_embed.title.rfind('(')+1:old_embed.title.rfind(')')]) not in thumbnails:
            embed = Embed(title=" ",description="**:x: This submission does not exist!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to accept a thumbnail (does not exist)")
            return

        if f"{old_embed.title[old_embed.title.rfind('(')+1:old_embed.title.rfind(')')]}.png" not in files:
            embed = Embed(title=" ",description="**:x: This submission has expired!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            embed = Embed(title=old_embed.title, description=f'{old_embed.description}', color=15548997)
            embed.set_image(url=old_embed.image.url)
            embed.set_footer(text=f"{client.user.name}", icon_url=f"{client.user.avatar}")
            embed.timestamp = old_embed.timestamp
            await message.edit(embed=embed)
            log(f"(FAILED) {interaction.user} FAILED to reject a thumbnail (expired)")
            return
        
        await interaction.response.send_modal(rejectThumbnailForm(client, message))