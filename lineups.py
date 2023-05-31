import typer

from api.deepl_api import translate_en_sk
from api.fb_api import post_image_with_message
from scrapers.flashscore import get_lineups_info
from scrapers.lfc_fb import get_latest_image_url


def main():
    image_url = get_latest_image_url()
    time, opponent = get_lineups_info()
    en_prefix = f"Today at {time} we play against {opponent}"
    sk_prefix = translate_en_sk(en_prefix).replace("hráme", "nastúpime")
    message = f"📋 {sk_prefix} v takejto zostave. Vaše názory?"
    post_image_with_message(message, image_url)


if __name__ == "__main__":
    typer.run(main)
