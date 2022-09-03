#!/usr/bin/env python3
# -*- coding:Windows-1252 -*-

from dataclasses import dataclass
from enum import Enum
import logging
import requests
from typing import List

from player_name_utils import remove_special_char
from transfermarkt_player import TMPlayer


@dataclass
class Club:
    name: str
    id: int
    url: str


class Position(Enum):
    G = 1
    D = 2
    M = 3
    F = 4


class TransfermarktApiClient:

    _BASE_URL = "https://www.transfermarkt.com"
    _HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'cookie': 's_ga=GA1.2.974713430.1556589812; __gads=ID=2f635078c6e37fc5:T=1556589814:S=ALNI_MYBlZckdQFx6vD8iADC_aclVRvw-Q; TMSESSID=1jg57ttfian37t5q6loalfu066; _gid=GA1.2.792961174.1564539337; POPUPCHECK=1564625920497; ioam2018=001a4fbfad5e90b375cc7acf2:1584324212713:1556589812713:.transfermarkt.com:112:transfer:ausland_rest_r:noevent:1564565972027:i5qaft; utag_main=v_id:016a6bfb9b8e0022bbb662e25bb803069001e06100bd0$_sn:9$_ss:0$_st:1564567768238$dc_visit_transfermarkt-transfermarkt.de:7$dip_visitor_id:016a6bfbb144001aa0b25bd0ac8b03069001e06100bd0$dc_visit_dip-main:8$ses_id:1564564905485%3Bexp-session$_pn:4%3Bexp-session$collectCookieMode:3rdParty%3Bexp-session$dc_event_transfermarkt-transfermarkt.de:3%3Bexp-session$dip_events_this_session:4%3Bexp-session$dc_event_dip-main:4%3Bexp-session$dc_region_transfermarkt-transfermarkt.de:eu-central-1%3Bexp-session$dc_region_dip-main:eu-central-1%3Bexp-session'
    }
    
    @classmethod
    def get_clubs_from_league(cls, league_suffix) -> List[Club]:
        league_api_url = f"{cls._BASE_URL}/quickselect/teams/{league_suffix}"
        logging.info("Visit league: %s", league_api_url)
        # TODO: Add retry
        response = requests.get(league_api_url, headers=cls._HEADERS)
        league_info = response.json()
        res = []
        for team in league_info:
            team_name = remove_special_char(team['name'])
            team_url = f"{cls._BASE_URL}{team['link']}"
            res.append(Club(name=team_name, id=int(team['id']), url=team_url))
        return res

    @classmethod
    def get_players_from_club(cls, club: Club) -> List[TMPlayer]:
        logging.info("Visit club: %s %s", club.name, club.url)

        response = requests.get(f"{cls._BASE_URL}/quickselect/players/{club.id}",
                                headers=cls._HEADERS)
        player_list = []
        for player in response.json():
            player_name = remove_special_char(player['name'])
            position = Position(player['positionId']).name
            new_player = TMPlayer(name=player_name,
                                  position=position,
                                  club=club.name,
                                  number=int(player['shirtNumber']),
                                  unique_id=int(player['id']))
            player_list.append(new_player)
            # print(new_player.to_csv_line(new_line=False))
    
        return player_list
