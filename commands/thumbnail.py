from discord import Interaction, Embed, Attachment
from util.functions import log
from json import load
from requests import get, post
from datetime import datetime
from json import dump
from PIL import Image
from util.translate import get_language, translate

def commandFunction(tree, client):
    @tree.command(name="thumbnail",description="Submit a thumbnail for an in-game level")
    async def thumbnailCommand(interaction: Interaction, level: int, image: Attachment):
        lang = get_language(interaction.user.id)
        with open("specialConfig.json", "r") as specialConfigFile:
            data = load(specialConfigFile)
            server = data["server"]
            databaseUrl = data["databaseUrl"]
            thumbnailsChannel = data["thumbnailsChannel"]
            verifiedThumbnailerRole = data["verifiedThumbnailerRole"]
        
        with open("thumbnails.json", "r") as thumbnailsFile:
            thumbnailsData = load(thumbnailsFile)
            thumbnails = thumbnailsData.get("thumbnails", [])

        if interaction.guild.id != server:
            embed = Embed(title=" ",description=f"**:x: {translate('cmd.error.not_here', lang)}**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to post a thumbnail (not allowed)")
            return

        if thumbnailsChannel == None or thumbnailsChannel == 0 or verifiedThumbnailerRole == 0:
            embed = Embed(title=" ",description=f"**:x: {translate('cmd.error.config', lang)}**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to post a thumbnail (not configured)")
            return
  
        if not image.filename.endswith(".png"):
            embed = Embed(title=" ",description=f"**:x: {translate('cmd.error.image.not_png', lang)}**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to post a thumbnail (not a .png file)")
            return
        if image.width == None or image.height == None:
            embed = Embed(title=" ",description=f"**:x: {translate('cmd.error.image.malformed', lang)}**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to post a thumbnail (malformed)")
            return
        if image.width < 1920 or image.height < 1080:
            embed = Embed(title=" ",description=f"**:x: {translate('cmd.error.image.under_1920x1080', lang)}**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to post a thumbnail (not above 1920x1080)")
            return
        
        if abs((image.width / image.height) - (16 / 9)) > 0.01: #tolerance value, width can be 16/9 * height ± tolerance * height
            embed = Embed(title=" ",description=f"**:x: {translate('cmd.error.image.not_16b9', lang)}**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to post a thumbnail (not 16:9)")
            return

        if level in thumbnails:
            embed = Embed(title=" ",description=f"**:x: {translate('cmd.error.thumb.already_suggested', lang)}**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to post a thumbnail (already suggested)")
            return
            
        else:
            headers = {
                "User-Agent": ""
            }

            data = {
                "str": level,
                "type": 0,
                "secret": "Wmfd2893gb7"
            }

            req = post(url=f"{databaseUrl}/getGJLevels21.php", data=data, headers=headers)

            if req.status_code != 200:
                embed = Embed(title=" ",description=f"**:x: {translate('error.server.fetch_level_fail', lang)}**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to post a thumbnail (failed to fetch the level from the servers)")
                return

            levelName = req.text.split("2:")[1].split(':')[0]
            levelAuthor = req.text.split('#')[1].split(':')[1]

            try:
                with open(f"thumbnails/{level}.png", "wb") as f:
                    f.write((get(image.url)).content)

                thumbnails.append(level)
                json_dict = {"thumbnails": thumbnails}
                with open("thumbnails.json", "w") as thumbnailsFile:
                    dump(json_dict, thumbnailsFile, indent=4)
            except:
                embed = Embed(title=" ",description=f"**:x: {translate('error.generic', lang)}**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to post a thumbnail (error when saving the image/writting in the json file)")
                return
            
            if image.width > 1920 and image.height > 1080:
                resizedImage = Image.open(f"thumbnails/{level}.png")
                resizedImage = resizedImage.resize((1920, 1080))
                resizedImage.save(f"thumbnails/{level}.png")

            embed = Embed(title=f"{levelName} by {levelAuthor} ({level})",description=f"By <@{interaction.user.id}> ({interaction.user.id})")
            embed.set_image(url=f"{image.url}")
            embed.set_footer(text=f"{client.user.name}", icon_url=f"{client.user.avatar}")
            embed.timestamp = datetime.now()

            try:
                channel = client.get_channel(thumbnailsChannel)
                await channel.send(f"<@&{verifiedThumbnailerRole}>",embed=embed)
                embed = Embed(title=" ",description=f"**:white_check_mark: {translate('cmd.thumb.success', lang)}**",colour=2067276)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(SUCCESS) {interaction.user} POSTED a thumbnail")  

            except:
                embed = Embed(title=" ",description=f"**:x: {translate('error.generic', lang)}**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to post a thumbnail (could not post in the channel/could not reply)")
                return