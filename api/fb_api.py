import os

import requests
from dotenv import load_dotenv

load_dotenv("../.env")


def post_image_with_message(message: str, image_url: str):
    page_id = os.getenv("PAGE_ID")
    access_token = os.getenv("PAGE_ACCESS_TOKEN")
    image_data = {"url": image_url, "access_token": access_token, "message": message}
    url = f"https://graph.facebook.com/{page_id}/photos"
    response = requests.post(url, data=image_data)

    if response.status_code == 200:
        print("Post published successfully!")
        return response.json()

    print("Error publishing post.")


def post_message(message: str):
    page_id = os.getenv("PAGE_ID")
    access_token = os.getenv("PAGE_ACCESS_TOKEN")
    url = f"https://graph.facebook.com/{page_id}/feed"
    response = requests.post(
        url, data={"access_token": access_token, "message": message}
    )

    if response.status_code == 200:
        print("Post published successfully!")
        return response.json()
    print("Error publishing post.")
