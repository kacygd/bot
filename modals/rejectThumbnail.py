from discord.ui import Modal, TextInput
from discord import Embed, TextStyle, Interaction
from util.functions import log
from os import listdir, remove
from json import load, dump
from datetime import datetime

class rejectThumbnailForm(Modal, title='Reject Thumbnail'):
    def __init__(self, client, message):
        self.client = client
        self.message = message
        super().__init__()
    input_0 = TextInput(label="Rejection Reason",placeholder="Explain why the thumbnail was rejected (optional)",style=TextStyle.long, required=False)
    async def on_submit(self, interaction: Interaction):
        with open("thumbnails.json", "r") as thumbnailsFile:
            thumbnailsData = load(thumbnailsFile)
            thumbnails = thumbnailsData.get("thumbnails", [])
        file_array = listdir("thumbnails")

        message = await interaction.channel.fetch_message(self.message.id)

        old_embed = message.embeds[0]

        levelID = int(old_embed.title[old_embed.title.rfind('(')+1:old_embed.title.rfind(')')])
        submissionAuthor = await self.client.fetch_user(int(old_embed.description[old_embed.description.rfind('(')+1:old_embed.description.rfind(')')]))
        if self.input_0.value == "":
            embed = Embed(title=f"**Your thumbnail submission (ID: ``{levelID}``) was rejected!**",description="", colour=15548997)
            embed.set_image(url=old_embed.image.url)
            embed.set_footer(text=f"{self.client.user.name}", icon_url=f"{self.client.user.avatar}")
            embed.timestamp = datetime.now()
            try:
                await submissionAuthor.send(" ",embed=embed)
            except:
                embed = Embed(title=f"**Your thumbnail submission (ID: ``{levelID}``) was rejected!**",description="", colour=15548997)
            embed = Embed(title=" ",description=f"**``{levelID}`` has been rejected!**", colour=5763719)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(SUCCESS) {interaction.user} REJECTED thumbnail ID {levelID}")

            embed = Embed(title=old_embed.title, description=f'{old_embed.description}', color=15548997)
            embed.set_image(url=old_embed.image.url)
            embed.set_footer(text=f"{self.client.user.name}", icon_url=f"{self.client.user.avatar}")
            embed.timestamp = old_embed.timestamp

            try:
                await message.edit(embed=embed)
            except:
                embed = Embed(title=" ",description=":x: **An error occurred while trying to edit the message**", colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAIL) {interaction.user} failed to use the reject thumbnail form (could not edit the message)")
                return

            try:
                for file in file_array:
                    file_path = f"thumbnails/{file}"
                    if file_path == f"thumbnails/{levelID}.png":
                        remove(file_path)
            except:
                embed = Embed(title=" ",description=":x: **An error occurred while trying to remove the image**", colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAIL) {interaction.user} failed to use the reject thumbnail form (could not remove the image)")
                return
                
            try:
                thumbnails.remove(levelID)
                json_dict = {"thumbnails": thumbnails}
                with open("thumbnails.json", "w") as thumbnailsFile:
                    dump(json_dict, thumbnailsFile, indent=4)
            except:
                embed = Embed(title=" ",description=":x: **An error occurred while trying to remove the thumbnail ID from the JSON file**", colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAIL) {interaction.user} failed to use the reject thumbnail form (could not remove the thumbnail ID from the json file)")
                return
                
        else:
            embed = Embed(title=f"**Your thumbnail submission (ID: ``{levelID}``) was rejected!**\n``Reason: {self.input_0.value}``",description="", colour=15548997)
            embed.set_image(url=old_embed.image.url)
            embed.set_footer(text=f"{self.client.user.name}", icon_url=f"{self.client.user.avatar}")
            embed.timestamp = datetime.now()
            await submissionAuthor.send(" ",embed=embed)
            embed = Embed(title=" ",description=f"**``{levelID}`` has been rejected!**", colour=5763719)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            
            embed = Embed(title=old_embed.title, description=f'{old_embed.description}', color=15548997)
            embed.set_image(url=old_embed.image.url)
            embed.set_footer(text=f"{self.client.user.name}", icon_url=f"{self.client.user.avatar}")
            embed.timestamp = old_embed.timestamp

            try:
                await message.edit(embed=embed)
            except:
                embed = Embed(title=" ",description=":x: **An error occurred while trying to edit the message**", colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAIL) {interaction.user} failed to use the reject thumbnail form (could not edit the message)")
                return

            try:
                for file in file_array:
                    file_path = f"thumbnails/{file}"
                    if file_path == f"thumbnails/{levelID}.png":
                        remove(file_path)
            except:
                embed = Embed(title=" ",description=":x: **An error occurred while trying to remove the image**", colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAIL) {interaction.user} failed to use the reject thumbnail form (could not remove the image)")
                return

            try:
                thumbnails.remove(levelID)
                json_dict = {"thumbnails": thumbnails}
                with open("thumbnails.json", "w") as thumbnailsFile:
                    dump(json_dict, thumbnailsFile, indent=4)
            except:
                embed = Embed(title=" ",description=":x: **An error occurred while trying to remove the thumbnail ID from the JSON file**", colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAIL) {interaction.user} failed to use the reject thumbnail form (could not remove the thumbnail ID from the json file)")
                return
            
            log(f"(SUCCESS) {interaction.user} REJECTED thumbnail (ID: {levelID}) and gave a reason")