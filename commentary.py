import time
from enum import Enum

import typer

from api.fb_api import post_message
from scrapers.flashscore import scrape_fs_page, get_match_info_url

LAST_INCIDENT_POSTED = -1


class IncidentType(Enum):
    LFC_GOAL = 1
    OPPONENT_GOAL = 2
    LFC_RED_CARD = 3
    OPPONENT_RED_CARD = 4
    LFC_VAR_DISSALOWED = 5
    OPPONENT_VAR_DISSALOWED = 6
    LFC_PENALTY_MISSED = 7
    OPPONENT_PENALTY_MISSED = 8
    OTHER = 9


def post_comment(incident: dict):
    if incident["type"] == IncidentType.LFC_GOAL:
        message = f"""⚽ GÓÓÓÓÓÓÓÓÓÓÓÓÓL!!!
        {incident['time']}' {incident['player']} {incident['assist']}
        {incident['home_score']}-{incident['away_score']}
        """
    elif incident["type"] == IncidentType.OPPONENT_GOAL:
        message = f"""⚽ Gól!
        {incident['time']}' {incident['player']}
        {incident['home_score']}-{incident['away_score']}
        """
    # TODO: Add support for other incidents
    # elif incident["type"] == IncidentType.LFC_RED_CARD:
    #     message = ""
    # elif incident["type"] == IncidentType.OPPONENT_RED_CARD:
    #     message = ""
    # elif incident["type"] == IncidentType.LFC_PENALTY_MISSED:
    #     message = ""
    # elif incident["type"] == IncidentType.OPPONENT_PENALTY_MISSED:
    #     message = ""
    else:
        return None
    post_message(message)


def comment_the_match(url: str):
    global LAST_INCIDENT_POSTED
    while True:
        soup = scrape_fs_page(url)
        status = soup.find(class_="fixedHeaderDuel__detailStatus").text
        if status == "Prestávka" or status == "Koniec":
            break
        is_lfc_home_team = (
            soup.find(class_="participant__participantName").text == "Liverpool"
        )
        score = soup.find(class_="detailScore__wrapper").text
        home_score, away_score = score.split("-")
        incident_tags = soup.find_all(class_="smv__participantRow")
        incidents = []
        for incident_tag in incident_tags:
            incident = {
                "time": incident_tag.find(class_="smv__timeBox").text[:-1],
                "home_score": home_score,
                "away_score": away_score,
                "player": incident_tag.find(class_="smv__playerName").text,
            }

            if incident_tag.find(class_="smv__incidentAwayScore") is not None:
                incident["type"] = (
                    IncidentType.OPPONENT_GOAL
                    if is_lfc_home_team
                    else IncidentType.LFC_GOAL
                )
                assist = incident_tag.find(class_="smv__assist")
                incident["assist"] = assist.text if assist is not None else ""
                incidents.append(incident)
            elif incident_tag.find(class_="smv__incidentHomeScore") is not None:
                incident["type"] = (
                    IncidentType.LFC_GOAL
                    if is_lfc_home_team
                    else IncidentType.OPPONENT_GOAL
                )
                assist = incident_tag.find(class_="smv__assist")
                incident["assist"] = assist.text if assist is not None else ""
                incidents.append(incident)
            # TODO: Add support for other incidents
            else:
                incident["type"] = IncidentType.OTHER
        for i in range(LAST_INCIDENT_POSTED + 1, len(incidents)):
            post_comment(incidents[i])
        LAST_INCIDENT_POSTED = len(incidents) - 1
    time.sleep(60)


def main():
    url = get_match_info_url()
    # First half
    comment_the_match(url)
    time.sleep(60 * 15)
    # Second half
    comment_the_match(url)


if __name__ == "__main__":
    typer.run(main)
