from discord import Interaction, Embed, Attachment
from util.functions import log
from json import load
from requests import get, post
from datetime import datetime
from json import dump

def commandFunction(tree, client):
    @tree.command(name="thumbnail",description="Submit a thumbnail for an in-game level")
    async def thumbnailCommand(interaction: Interaction, level: int, image: Attachment):
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
            embed = Embed(title=" ",description="**:x: You are not allowed to use this here!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to post a thumbnail (not allowed)")
            return

        if thumbnailsChannel == 0 or verifiedThumbnailerRole == 0:
            embed = Embed(title=" ",description="**:x: This command has not yet been configured.**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to post a thumbnail (not configured)")
            return

        if thumbnailsChannel == None:
            embed = Embed(title=" ",description="**:x: This command has not yet been configured.**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to post a thumbnail (not configured)")
            return
  
        if not image.filename.endswith(".png"):
            embed = Embed(title=" ",description="**:x: This image is not a .png file!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to post a thumbnail (not a .png file)")
            return

        if (image.width / image.height) < (16 / 9):
            embed = Embed(title=" ",description="**:x: This image is not 16:9!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to post a thumbnail (not 16:9)")
            return
            
        if image.width > 1920 or image.height > 1080:
            embed = Embed(title=" ",description="**:x: This image is not 1920x1080!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to post a thumbnail (not 16:9)")
            return

        if level in thumbnails:
            embed = Embed(title=" ",description="**:x: This thumbnail has already been suggested!**",colour=15548997)
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
                embed = Embed(title=" ",description="**:x: Failed to fetch the level from the servers**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to post a thumbnail (failed to fetch the level from the servers)")
                return

            levelName = "Unknown"
            levelAuthor = "Unknown"

            sections = req.text.split('#')

            for value in sections[0].split(':'):
                if value == "2":
                    levelName = sections[0].split(':')[sections[0].split(':').index(value) + 1]

            for value in sections[1].split(':'):
                if value == "2":
                    levelAuthor = sections[1].split(':')[sections[1].split(':').index(value) + 1]

            try:
                with open(f"thumbnails/{level}.png", "wb") as f:
                    f.write((get(image.url)).content)

                thumbnails.append(level)
                json_dict = {"thumbnails": thumbnails}
                with open("thumbnails.json", "w") as thumbnailsFile:
                    dump(json_dict, thumbnailsFile, indent=4)
            except:
                embed = Embed(title=" ",description="**:x: An error occured**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to post a thumbnail (error when saving the image/writting in the json file)")
                return

            embed = Embed(title=f"{levelName} by {levelAuthor} ({level})",description=f"By <@{interaction.user.id}> ({interaction.user.id})")
            embed.set_image(url=f"{image.url}")
            embed.set_footer(text=f"{client.user.name}", icon_url=f"{client.user.avatar}")
            embed.timestamp = datetime.now()

            try:
                channel = client.get_channel(thumbnailsChannel)
                await channel.send(f"<@&{verifiedThumbnailerRole}>",embed=embed)
                embed = Embed(title=" ",description="**:white_check_mark: Successfully posted a thumbnail!**",colour=2067276)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(SUCCESS) {interaction.user} POSTED a thumbnail")  

            except:
                embed = Embed(title=" ",description="**:x: An error occured**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to post a thumbnail (could not post in the channel/could not reply)")
                return