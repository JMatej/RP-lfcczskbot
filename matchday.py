import typer

from api.fb_api import post_image_with_message
from scrapers.flashscore import get_match_info_url, get_pre_match_info

from scrapers.lfc_fb import get_latest_image_url


def main():
    fs_match_info_url = get_match_info_url()
    pre_match_info = get_pre_match_info(fs_match_info_url)
    image_url = get_latest_image_url()
    post_image_with_message(pre_match_info, image_url)


if __name__ == "__main__":
    typer.run(main)
