import time

from bs4 import BeautifulSoup
from dotenv import load_dotenv

from playwright.sync_api import sync_playwright

load_dotenv("../.env")


def get_latest_fb_post_url() -> str:
    url = "https://www.facebook.com/LiverpoolFC/"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        time.sleep(2)
        button_div = page.query_selector('div[aria-label="Decline optional cookies"]')
        button_div.click()

        time.sleep(1)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(3)
        page_content = page.content()
        browser.close()

    soup = BeautifulSoup(page_content, "html.parser")

    post = soup.find(class_="x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z")
    post_a = post.find(
        class_="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm"
    )
    post_href = post_a.get("href").split("?")[0]
    return post_href


def get_latest_fb_photo_url(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        time.sleep(1)
        button_selector = 'button[data-cookiebanner="accept_only_essential_button"]'
        page.click(button_selector)
        time.sleep(2)
        page_content = page.content()
        browser.close()

    soup = BeautifulSoup(page_content, "html.parser")
    image_tag = soup.find(class_="_4-eo _2t9n _50z9")
    return "https://www.facebook.com" + image_tag.get("href").split("?")[0]


def get_image_url(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        time.sleep(1)
        button_div = page.query_selector('div[aria-label="Decline optional cookies"]')
        button_div.click()
        time.sleep(1)
        page_content = page.content()
        browser.close()

    soup = BeautifulSoup(page_content, "html.parser")
    image_tag = soup.find(class_="x85a59c x193iq5w x4fas0m x19kjcj4")

    return image_tag.get("src")


def get_latest_image_url():
    latest_fb_post_url = get_latest_fb_post_url()
    latest_fb_photo_url = get_latest_fb_photo_url(latest_fb_post_url)
    latest_image_url = get_image_url(latest_fb_photo_url)
    return latest_image_url
