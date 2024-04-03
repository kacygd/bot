from discord.ui import Modal, TextInput
from discord import Embed, TextStyle, Interaction
from util.functions import log
from os import remove
from requests import put
from util.resources import GITHUB_TOKEN
from json import dumps
from base64 import b64encode
from datetime import datetime

class acceptThumbnailForm(Modal, title='Accept Thumbnail'):
    def __init__(self, client, message):
        self.client = client
        self.message = message
        super().__init__()
    input_0 = TextInput(label="Notes",placeholder="Any additional notes?",style=TextStyle.long, required=False)
    async def on_submit(self, interaction: Interaction):

        message = await interaction.channel.fetch_message(self.message.id)

        old_embed = message.embeds[0]

        levelID = int(old_embed.title[old_embed.title.rfind('(')+1:old_embed.title.rfind(')')])
        submissionAuthor = await self.client.fetch_user(int(old_embed.description[old_embed.description.rfind('(')+1:old_embed.description.rfind(')')]))
        if self.input_0.value == "":
            with open(f"thumbnails/{levelID}.png", "rb") as thumbnailFile:
                thumbnail = thumbnailFile.read()

            headers = {
                'Authorization': f'token {GITHUB_TOKEN}',
                'Accept': 'application/vnd.github.v3+json',
            }

            data = {
                'message': f"[BOT] Added thumbnail for {levelID} by {submissionAuthor}",
                'content': b64encode(thumbnail).decode('utf-8'),
                'branch': 'main'
            }

            response = put(f'https://api.github.com/repos/PlusGDPS/level-thumbnails/contents/thumbs/{levelID}.png', headers=headers, data=dumps(data))
            
            if response.status_code != 200 and response.status_code != 201:
                embed = Embed(title=" ",description="<:x:1039888272761049179> **An error occurred while trying to post the thumbnail**", colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAIL) {interaction.user} failed to accept a thumbnail (error with GitHub API)")
                return
            
            embed = Embed(title=f"**Your thumbnail submission (ID: ``{levelID}``) was accepted!**",description="", colour=2067276)
            embed.set_image(url=old_embed.image.url)
            embed.set_footer(text=f"{self.client.user.name}", icon_url=f"{self.client.user.avatar}")
            embed.timestamp = datetime.now()

            try:
                await submissionAuthor.send(" ",embed=embed)
            except:
                pass
            embed = Embed(title=" ",description=f"**``{levelID}`` has been accepted!**", colour=5763719)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)

            embed = Embed(title=old_embed.title, description=f'{old_embed.description}', color=2067276)
            embed.set_image(url=old_embed.image.url)
            embed.set_footer(text=f"{self.client.user.name}", icon_url=f"{self.client.user.avatar}")
            embed.timestamp = old_embed.timestamp

            await message.edit(embed=embed)

            remove(f"thumbnails/{levelID}.png")

            log(f"(SUCCESS) {interaction.user} ACCEPTED a thumbnail (ID: {levelID})")
        else:
            with open(f"thumbnails/{levelID}.png", "rb") as thumbnailFile:
                thumbnail = thumbnailFile.read()

            headers = {
                'Authorization': f'token {GITHUB_TOKEN}',
                'Accept': 'application/vnd.github.v3+json',
            }

            data = {
                'message': f"[BOT] Added thumbnail for {levelID} by {submissionAuthor}",
                'content': b64encode(thumbnail).decode('utf-8'),
                'branch': 'main'
            }

            response = put(f'https://api.github.com/repos/PlusGDPS/level-thumbnails/contents/thumbs/{levelID}.png', headers=headers, data=dumps(data))
            
            if response.status_code != 200 and response.status_code != 201:
                embed = Embed(title=" ",description="<:x:1039888272761049179> **An error occurred while trying to post the thumbnail**", colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAIL) {interaction.user} failed to accept a thumbnail (error with GitHub API)")
                return
            
            embed = Embed(title=f"**Your thumbnail submission (ID: ``{levelID}``) was accepted!**\n``Additional notes: {self.input_0.value}``",description="", colour=2067276)
            embed.set_image(url=old_embed.image.url)
            embed.set_footer(text=f"{self.client.user.name}", icon_url=f"{self.client.user.avatar}")
            embed.timestamp = datetime.now()

            try:
                await submissionAuthor.send(" ",embed=embed)
            except:
                pass
            embed = Embed(title=" ",description=f"**``{levelID}`` has been accepted!**", colour=5763719)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)

            embed = Embed(title=old_embed.title, description=f'{old_embed.description}', color=2067276)
            embed.set_image(url=old_embed.image.url)
            embed.set_footer(text=f"{self.client.user.name}", icon_url=f"{self.client.user.avatar}")
            embed.timestamp = old_embed.timestamp

            await message.edit(embed=embed)

            remove(f"thumbnails/{levelID}.png")
            
            log(f"(SUCCESS) {interaction.user} ACCEPTED a thumbnail (ID: {levelID}) and added a note")