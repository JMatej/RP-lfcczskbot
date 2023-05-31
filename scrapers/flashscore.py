from typing import Tuple

from bs4 import BeautifulSoup
from dotenv import load_dotenv

from playwright.sync_api import sync_playwright

load_dotenv("../.env")


def scrape_fs_page(url: str) -> BeautifulSoup:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        page.click("#onetrust-accept-btn-handler")
        page_content = page.content()
        browser.close()

    return BeautifulSoup(page_content, "html.parser")


def get_pre_match_info(url: str) -> str:
    soup = scrape_fs_page(url)

    competition = soup.find("span", class_="tournamentHeader__country").find("a").text
    home_team, away_team = [
        team.text for team in soup.find_all("a", class_="participant__participantName")
    ]
    start_time = soup.find("div", class_="duelParticipant__startTime").text.split()[-1]
    stadium = soup.find_all(class_="mi__item__val")[-1].text
    broadcast = soup.find(class_="br__row").text

    return (
        f"#MATCHDAY\n"
        f"🏆 {competition}\n"
        f"⚽ {home_team} - {away_team}\n"
        f"🏟️ {stadium}\n"
        f"🕖 {start_time}\n"
        f"📺 {broadcast}\n\n"
        f"Aký tipujete výsledok zápasu?"
    )


def get_match_info_url() -> str:
    soup = scrape_fs_page("https://www.flashscore.sk/")
    matches = soup.find_all(class_="event__match--twoLine")
    the_team = "Liverpool"

    for match in matches:
        home_team = match.find(class_="event__participant--home").text
        away_team = match.find(class_="event__participant--away").text

        if the_team in home_team or the_team in away_team:
            match_id = match.get("id")[-8:]
            return f"https://www.flashscore.sk/zapas/{match_id}/#/prehlad-zapasu"


def get_lineups_info() -> Tuple[str, str]:
    soup = scrape_fs_page("https://www.flashscore.sk/")
    matches = soup.find_all(class_="event__match--twoLine")
    the_team = "Liverpool"

    for match in matches:
        home_team = match.find(class_="event__participant--home").text
        away_team = match.find(class_="event__participant--away").text

        if the_team in home_team or the_team in away_team:
            time = match.find(class_="event__time").text
            opponent = home_team if the_team in away_team else away_team
            return time, opponent
