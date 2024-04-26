from discord import Interaction, Message, Embed
from json import load
from util.translate import translate
from util.functions import log
from os import listdir

async def action(interaction:Interaction, message:Message, action:str, lang:str, client) -> bool:
    with open("specialConfig.json", "r") as specialConfigFile:
        specialConfig = load(specialConfigFile)
    with open("thumbnails.json", "r") as thumbnailsFile:
        thumbnailsData = load(thumbnailsFile)
        thumbnails = thumbnailsData.get("thumbnails", [])

    files = listdir("thumbnails")        
    member = await interaction.guild.fetch_member(interaction.user.id)
    old_embed = message.embeds[0]

    if interaction.guild.id != specialConfig["server"]:
        embed = Embed(title=" ",description=f"**:x: {translate("cmd.error.not_here", lang)}**",colour=15548997)
        await interaction.response.send_message(" ",embed=embed, ephemeral=True)
        log(f"(FAILED) {interaction.user} FAILED to {action} a thumbnail (not allowed)")
        return False
    
    if not any(role.id == specialConfig["verifiedThumbnailerRole"] for role in member.roles):
        embed = Embed(title=" ",description=f"**:x: {translate("error.no_permission", lang)}**",colour=15548997)
        await interaction.response.send_message(" ",embed=embed, ephemeral=True)
        log(f"(FAILED) {interaction.user} FAILED to {action} a thumbnail (not allowed)")
        return False
    
    if message.author.id != client.user.id:
        embed = Embed(title=" ",description=f"**:x: {translate("context.error.not_by_bot", lang)}**",colour=15548997)
        await interaction.response.send_message(" ",embed=embed, ephemeral=True)
        log(f"(FAILED) {interaction.user} FAILED to {action} a thumbnail (wrong message)")
        return False
    
    if not (old_embed.title[old_embed.title.rfind('(')+1:old_embed.title.rfind(')')].isdigit() and old_embed.description[old_embed.description.rfind('(')+1:old_embed.description.rfind(')')].isdigit()):
        embed = Embed(title=" ",description=f"**:x: {translate("error.msg.invalid", lang)}**",colour=15548997)
        await interaction.response.send_message(" ",embed=embed, ephemeral=True)
        log(f"(FAILED) {interaction.user} FAILED to {action} a thumbnail (invalid message)")
        return False
    
    if str(old_embed.color) == "#ed4245":
        embed = Embed(title=" ",description=f"**:x: {translate("context.error.already_rejected", lang)}**",colour=15548997)
        await interaction.response.send_message(" ",embed=embed, ephemeral=True)
        log(f"(FAILED) {interaction.user} FAILED to {action} a thumbnail (already rejected)")
        return False

    if str(old_embed.color) == "#1f8b4c":
        embed = Embed(title=" ",description=f"**:x: {translate("context.error.already_accepted", lang)}**",colour=15548997)
        await interaction.response.send_message(" ",embed=embed, ephemeral=True)
        log(f"(FAILED) {interaction.user} FAILED to {action} a thumbnail (already accepted)")
        return False

    if int(old_embed.title[old_embed.title.rfind('(')+1:old_embed.title.rfind(')')]) not in thumbnails:
        embed = Embed(title=" ",description=f"**:x: {translate("context.error.submission.nonexist", lang)}**",colour=15548997)
        await interaction.response.send_message(" ",embed=embed, ephemeral=True)
        embed = Embed(title=old_embed.title, description=f'{old_embed.description}', color=15548997)
        embed.set_image(url=old_embed.image.url)
        embed.set_footer(text=f"{client.user.name}", icon_url=f"{client.user.avatar}")
        embed.timestamp = old_embed.timestamp
        await message.edit(embed=embed)
        log(f"(FAILED) {interaction.user} FAILED to {action} a thumbnail (does not exist)")
        return False
    
    if f"{old_embed.title[old_embed.title.rfind('(')+1:old_embed.title.rfind(')')]}.png" not in files:
        embed = Embed(title=" ",description=f"**:x: {translate("context.error.submission.expire", lang)}**",colour=15548997)
        await interaction.response.send_message(" ",embed=embed, ephemeral=True)
        embed = Embed(title=old_embed.title, description=f'{old_embed.description}', color=15548997)
        embed.set_image(url=old_embed.image.url)
        embed.set_footer(text=f"{client.user.name}", icon_url=f"{client.user.avatar}")
        embed.timestamp = old_embed.timestamp
        await message.edit(embed=embed)
        log(f"(FAILED) {interaction.user} FAILED to {action} a thumbnail (expired)")
        return False
    return True