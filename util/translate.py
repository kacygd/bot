from json import load, dump
from util.functions import log
import os

user_lang = {}
lang_data = {}

def initialize():
    files = os.listdir("data/lang")
    for file in files:
        if not os.path.isfile("data/lang/" + file):
            continue
        fs = file.split(".")
        if not fs[1] == "json":
            continue
        with open("data/lang/" + file, "r", encoding="utf8") as lang_file:
            lang_data[fs[0]] = load(lang_file)
    with open ("data/user_lang.json", "r") as user_lang_file:
        user_lang = load(user_lang_file)

initialize()

def translate(value:str, language:str) -> str:
    try:
        return lang_data[language][value]
    except KeyError:
        log(f"(WARN) Unable to translate {value} into {language}")
        try:
            return lang_data["en_uk"][value]
        except KeyError:
            log(f"(FAIL) Unable to translate {value}")
            return value

def set_language(user_id:int, language:str, auto:bool):
    with open ("data/user_lang.json", "w") as lang_file:
        user_lang[str(user_id)] = {"lang":language,"auto":auto}
        dump(user_lang, lang_file)

def get_language(user_id:int, locale:str) -> str:
    if (not str(user_id) in user_lang) or (user_lang[str(user_id)]["auto"] and locale != None):
        set_language(user_id, get_from_locale(locale), True)
    return user_lang[str(user_id)]["lang"]
def get_language_default(user_id:int) -> str:
    return get_language(user_id, None)
def get_from_locale(locale:str) -> str:
    for lang in lang_data.keys():
        if locale in lang_data[lang]["default"]:
            return lang
    return "en_uk"
