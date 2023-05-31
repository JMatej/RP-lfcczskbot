import os
import deepl

from dotenv import load_dotenv

load_dotenv("../.env")


def translate_en_sk(message: str) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(message, target_lang="SK")
    return result.text
