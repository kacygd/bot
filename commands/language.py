from discord import Interaction, Embed, ButtonStyle
from discord.ui import View, Button
from discord.app_commands import default_permissions
from util.functions import log
from json import load, dump
from util.translate import *

def ifExp(lang:str) -> str:
    if translate("experimental", lang):
        return "\nTHIS LANGUAGE IS **EXPERIMENTAL** AND MAY CONTAIN **TRANSLATION ERRORS**"
    return ""
def ifCredit(lang:str) -> str:
    credit = translate("credit", lang)
    if credit is None:
        return ""
    return f"\n{translate('lang.translator', lang)} {credit}"

def get_embed(lang:str) -> Embed:
    return Embed(title=translate('lang.select.title', lang),description=f"{translate('lang.select.current', lang)} **{translate('name', lang)}**{ifCredit(lang)}{ifExp(lang)}\n\n{translate('lang.select.below', lang)}")
class LButton(Button):
    def __init__(self, lang:str, dis:bool):
        super().__init__(label=translate('name',lang),emoji=translate('icon',lang),style=ButtonStyle.gray,disabled=dis)
        self.lang = lang
    async def callback(self, interaction:Interaction):
        set_language(interaction.user.id, self.lang, False)
        await interaction.response.edit_message(embed=get_embed(self.lang),view=LView(self.lang))

class LView(View):
    def __init__(self, lang:str):
        super().__init__()
        for language in lang_data.keys():
            self.add_item(LButton(language, language==lang))

def commandFunction(tree, client):
    @tree.command(name="language",description="Change your selected language")
    async def languageCommand(interaction: Interaction):
        lang = get_language(interaction.user.id, interaction.locale.name)
        await interaction.response.send_message(embed=get_embed(lang),view=LView(lang),ephemeral=True)