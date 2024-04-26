from json import load, dump
from util.functions import log

with open ("data/lang.json", "r", encoding="utf8") as lang_file:
    lang_data = load(lang_file)
with open ("data/user_lang.json", "r") as user_lang_file:
    user_lang = load(user_lang_file)

def translate(value:str, language:str) -> str:
    try:
        return lang_data[language][value]
    except KeyError:
        log(f'WARN Unable to translate {value} into {language}')
        try:
            return lang_data["en_uk"][value]
        except KeyError:
            log(f'FAIL Unable to translate {value}')
            return value

def set_language(user_id:int, language:str):
    with open ("data/user_lang.json", "w") as lang_file:
        user_lang[f'{user_id}'] = language
        dump(user_lang, lang_file)

def get_language(user_id:int) -> str:
    if not f'{user_id}' in user_lang: set_language(user_id, "en_uk")
    return user_lang[f'{user_id}']