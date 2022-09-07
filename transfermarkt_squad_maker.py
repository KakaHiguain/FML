#!/usr/bin/env python3
# -*- coding:Windows-1252 -*-

import logging
from typing import List

from bs4 import BeautifulSoup

from common import *
from crawler import get_page
from transfermarkt_api_client import TransfermarktApiClient

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'cookie': 's_ga=GA1.2.974713430.1556589812; __gads=ID=2f635078c6e37fc5:T=1556589814:S=ALNI_MYBlZckdQFx6vD8iADC_aclVRvw-Q; TMSESSID=1jg57ttfian37t5q6loalfu066; _gid=GA1.2.792961174.1564539337; POPUPCHECK=1564625920497; ioam2018=001a4fbfad5e90b375cc7acf2:1584324212713:1556589812713:.transfermarkt.com:112:transfer:ausland_rest_r:noevent:1564565972027:i5qaft; utag_main=v_id:016a6bfb9b8e0022bbb662e25bb803069001e06100bd0$_sn:9$_ss:0$_st:1564567768238$dc_visit_transfermarkt-transfermarkt.de:7$dip_visitor_id:016a6bfbb144001aa0b25bd0ac8b03069001e06100bd0$dc_visit_dip-main:8$ses_id:1564564905485%3Bexp-session$_pn:4%3Bexp-session$collectCookieMode:3rdParty%3Bexp-session$dc_event_transfermarkt-transfermarkt.de:3%3Bexp-session$dip_events_this_session:4%3Bexp-session$dc_event_dip-main:4%3Bexp-session$dc_region_transfermarkt-transfermarkt.de:eu-central-1%3Bexp-session$dc_region_dip-main:eu-central-1%3Bexp-session'
}

BASE_URL = "https://www.transfermarkt.com"
TOP4_LEAGUE = {"Laliga": "ES1", "Premier League": "GB1", "Bundesliga": "L1", "Seria A": "IT1"}


# Main =============================================
def generate_fml_squad():
    csv_file = EXPORT_PATH / 'tmsquad-FML.csv'
    with csv_file.open("w") as f:
        f.write("Name,Position,Club,Number,Unique ID\n")
        for league_name, league_suffix in TOP4_LEAGUE.items():
            clubs = TransfermarktApiClient.get_clubs_from_league(league_suffix)
            for club in clubs:
                for player in TransfermarktApiClient.get_players_from_club(club):
                    f.write(player.to_csv_line())


# Deprecated
def read_ucl_page() -> List[List[str]]:
    UCL_URL = 'https://www.transfermarkt.com/champions-league/startseite/pokalwettbewerb/CL'
    ucl_page = get_page(UCL_URL, HEADERS)
    ucl_page_2 = ucl_page[ucl_page.find('<div class="table-header">Group table'):]
    soup = BeautifulSoup(ucl_page_2, features="html.parser")
    clubs = []
    for group in soup.find_all('a', attrs={'class': 'vereinprofil_tooltip'}):
        if not group.text:
            continue
        # Hack...
        club_url = str(group['href']).replace('spielplan', 'startseite')
        club = [str(group.text), BASE_URL + club_url]
        print(club)
        clubs.append(club)
    return clubs


def generate_fmc_squad():
    csv_file = EXPORT_PATH / 'tmsquad-FMC.csv'
    with csv_file.open("w") as f:
        f.write("Name,Position,Club,Number,Unique ID\n")
        clubs = TransfermarktApiClient.get_clubs_from_league("CL")
        for club in clubs:
            for player in TransfermarktApiClient.get_players_from_club(club):
                f.write(player.to_csv_line())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # generate_fml_squad()
    generate_fmc_squad()
