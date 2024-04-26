from discord import Interaction, Message
from modals.rejectThumbnail import rejectThumbnailForm
from util.translate import get_language
from util.thumbnail_action_ctx import action

def commandFunction(tree, client):
    @tree.context_menu(name="Reject Thumbnail")
    async def rejectThumbnail(interaction:Interaction, message: Message):
        message = await interaction.channel.fetch_message(message.id)
        lang = get_language(interaction.user.id)
        
        if not await action(interaction, message, "reject", lang, client): return
        
        await interaction.response.send_modal(rejectThumbnailForm(client, message, lang))