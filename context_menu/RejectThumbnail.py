from discord import Interaction, Embed, Message
from discord.app_commands import default_permissions
from util.functions import log
from modals.rejectThumbnail import rejectThumbnailForm
from json import load
from os import listdir

def commandFunction(tree, client):
    @tree.context_menu(name="Reject Thumbnail")
    @default_permissions(manage_messages=True)
    async def rejectThumbnail(interaction:Interaction, message: Message):
        with open("specialConfig.json", "r") as specialConfigFile:
            specialConfig = load(specialConfigFile)

        files = listdir("thumbnails")

        message = await interaction.channel.fetch_message(message.id)
        old_embed = message.embeds[0]
        submissionAuthor = old_embed.description[old_embed.description.rfind('(')+1:old_embed.description.rfind(')')]

        if interaction.guild.id != specialConfig["server"]:
            embed = Embed(title=" ",description="**:x: You cannot use this here!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to reject a thumbnail (not allowed)")
            return
        
        if message.author.id != client.user.id:
            embed = Embed(title=" ",description="**:x: This is not a message sent by the bot!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to reject a thumbnail (wrong message)")
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
        
        if str(old_embed.color) == "#1e1f22" and int(old_embed.description[old_embed.description.rfind('(')+1:old_embed.description.rfind(')')]) not in files:
            embed = Embed(title=" ",description="**:x: This submission has expired!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            embed = Embed(title=old_embed.title, description=f'{old_embed.description}', color=15548997)
            embed.set_image(url=old_embed.image.url)
            embed.set_footer(text=f"{client.user.name}", icon_url=f"{client.user.avatar}")
            embed.timestamp = old_embed.timestamp
            await message.edit(embed=embed)
            log(f"(FAILED) {interaction.user} FAILED to reject a thumbnail (expired)")
            return

        if str(old_embed.color) == "#ed4245":
            embed = Embed(title=" ",description="**:x: This submission has already been rejected!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to reject a thumbnail (already rejected)")
            return
        
        await interaction.response.send_modal(rejectThumbnailForm(client, message))