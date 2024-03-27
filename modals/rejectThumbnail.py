from discord.ui import Modal, TextInput
from discord import Embed, TextStyle, Interaction, Message
from util.functions import log

class rejectThumbnailForm(Modal, title='Reject Thumbnail'):
    def __init__(self, client, message):
        self.client = client
        self.message = message
        super().__init__()
    input_0 = TextInput(label="Rejection Reason",placeholder="Explain why the thumbnail was rejected (optional)",style=TextStyle.long, required=False)
    async def on_submit(self, interaction: Interaction):
        message = await interaction.channel.fetch_message(self.message.id)

        old_embed = message.embeds[0]

        levelID = int(old_embed.title[4:].strip())
        submissionAuthor = await self.client.fetch_user(int(old_embed.description[old_embed.description.rfind('(')+1:old_embed.description.rfind(')')]))

        #try:
        if self.input_0.value == "":
            embed = Embed(title=f"**Your thumbnail submission (ID: ``{levelID}``) was rejected!**",description="", colour=15548997)
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

            await message.edit(embed=embed)
                
        else:
            embed = Embed(title=f"**Your thumbnail submission (ID: ``{levelID}``) was rejected!**\n``Reason: {self.input_0.value}``",description="", colour=15548997)
            await submissionAuthor.send(" ",embed=embed)
            embed = Embed(title=" ",description=f"**``{levelID}`` has been rejected!**", colour=5763719)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(SUCCESS) {interaction.user} REJECTED thumbnail ID {levelID} and gave a reason")

            embed = Embed(title=old_embed.title, description=f'{old_embed.description}', color=15548997)
            embed.set_image(url=old_embed.image.url)
            embed.set_footer(text=f"{self.user.name}", icon_url=f"{self.user.avatar}")
            embed.timestamp = old_embed.timestamp

            await message.edit(embed=embed)
        
        #except:
            #embed = Embed(title=" ",description="<:x:1039888272761049179> **An error occurred**", colour=15548997)
            #await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            #log(f"(FAIL) {interaction.user} failed to use the reject thumbnail form")