from discord.ui import Modal, TextInput
from discord import TextStyle, Interaction, Embed, PartialEmoji, Emoji
from util.translate import translate
from requests import post
from json import load, dump
from util.functions import log
from datetime import datetime

def get_emoji(msg:str) -> dict:
    emoji = get_p_emoji(msg)
    if emoji == None:
        return {"poll_media":{"text":msg}}
    if emoji.is_custom_emoji():
        return {"poll_media":{"text":msg.split(" ")[1],"emoji":{"id":f"{emoji.id}"}}}
    return {"poll_media":{"text":msg.split(" ")[1],"emoji":{"name":emoji.name}}}
def get_p_emoji(msg:str) -> PartialEmoji:
    emoji = PartialEmoji.from_str(msg.split(" ")[0])
    if emoji.is_unicode_emoji():
        with open("data/emoji.json", "r") as file:
            emojis = load(file)["emojis"]
            if emoji.name in emojis:
                return emoji
            return None
    return emoji
        
class pollModal(Modal):
    def __init__(self, question:str, multiselect:bool, lang:str, channel:int, hours:int, client, message:str, placeholders:list[str]):
        self.question = question
        self.multiselect = multiselect
        self.lang = lang
        self.channel = channel
        self.hours = hours
        self.client = client
        self.message = message
        title = ""
        i = 0
        while(i < 45 and i < len(question)):
            title = title + question[i]
            i = i+1
        answer = translate("w.answer", lang)
        self.input_0.label = answer + " 1"
        self.input_1.label = answer + " 2"
        self.input_2.label = answer + " 3"
        self.input_3.label = answer + " 4"
        self.input_4.label = answer + " 5"
        self.input_0.placeholder = placeholders[0]
        self.input_1.placeholder = placeholders[1]
        self.input_2.placeholder = placeholders[2]
        self.input_3.placeholder = placeholders[3]
        self.input_4.placeholder = placeholders[4]
        super().__init__(title=title)
    input_0 = TextInput(label="",style=TextStyle.short, required=True)
    input_1 = TextInput(label="",style=TextStyle.short, required=True)
    input_2 = TextInput(label="",style=TextStyle.short, required=False)
    input_3 = TextInput(label="",style=TextStyle.short, required=False)
    input_4 = TextInput(label="",style=TextStyle.short, required=False)

    async def on_submit(self, interaction:Interaction):
        try:
            await interaction.response.defer(ephemeral=True)
            with open("config.json", "r") as config:
                token = load(config)["token"]
            headers = {'Content-Type':'application/json','Authorization':'Bot ' + token}
            answers = []
            answers.append(get_emoji(self.input_0.value))
            answers.append(get_emoji(self.input_1.value))
            if(len(self.input_2.value) > 0): answers.append(get_emoji(self.input_2.value))
            if(len(self.input_3.value) > 0): answers.append(get_emoji(self.input_3.value))
            if(len(self.input_4.value) > 0): answers.append(get_emoji(self.input_4.value))
            data = {"content":self.message,"poll":{"allow_multiselect":self.multiselect,"answers":answers,"duration":self.hours,"question":{"text":self.question}}}
            res = post(f"https://discord.com/api/v10/channels/{self.channel}/messages",headers=headers,json=data)
            if(200 != res.status_code):
                embed = Embed(title=" ",description=f"**:x: {translate('error.generic', self.lang)}**",colour=15548997)
                await interaction.followup.send(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to send a poll (API error)")
                return
            thread = await self.client.get_channel(self.channel).get_partial_message(int(res.json()["id"])).create_thread(name=self.question)   
            with open("data/threads.json", "r") as file:
                threads = load(file)
            threads["threads"].append({"time":int(datetime.now().timestamp())+self.hours*3600,"channel":self.channel,"thread":thread.id})
            with open("data/threads.json", "w") as file:
                dump(threads, file)
            embed = Embed(title=" ",description=f"**:white_check_mark: {translate('cmd.poll.success', self.lang)}**",colour=2067276)
            await interaction.followup.send(" ",embed=embed, ephemeral=True)
            log(f"(SUCCESS) {interaction.user} SENT a poll")
        except:
            embed = Embed(title=" ",description=f"**:x: {translate('error.generic', self.lang)}**",colour=15548997)
            await interaction.followup.send(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to send a poll (error)")