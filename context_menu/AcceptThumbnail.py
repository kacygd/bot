from discord import Interaction, Message
from modals.acceptThumbnail import acceptThumbnailForm
from util.translate import get_language
from util.thumbnail_action_ctx import action

def commandFunction(tree, client):
    @tree.context_menu(name="Accept Thumbnail")
    async def acceptThumbnail(interaction:Interaction, message: Message):
        message = await interaction.channel.fetch_message(message.id)
        lang = get_language(interaction.user.id)

        if not await action(interaction, message, "accept", lang, client): return
        
        await interaction.response.send_modal(acceptThumbnailForm(client, message, lang))