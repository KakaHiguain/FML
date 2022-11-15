#!/usr/bin/env python3
# -*- coding:Windows-1252 -*-

import logging
from typing import List, Dict, Set

from bs4 import BeautifulSoup

from common import *
from crawler import get_page
from player import Player
from player_name_utils import get_first_name_dict, get_unique_player_name


# TODO: refactor
def deduplicate_player_names(
        player_list: List[Player], first_name_dict: Dict[str, List[str]], final_player_names: Set[str]):
    for player in player_list:
        player.name = get_unique_player_name(player.name, first_name_dict)
        if player.name in final_player_names:
            logging.error('Still duplicate: %s', player.to_csv_line().rstrip())
        final_player_names.add(player.name)


class FootballSquadsSquadMaker:
    _BASE_URL = 'http://www.footballsquads.co.uk/'

    def get_squad(self, league_urls, output_path):
        team_url_dict = self._get_team_url_dict(league_urls)
        players = []
        for team_name, team_url in team_url_dict.items():
            league_page = get_page(self._BASE_URL + 'national/worldcup/' + team_url)
            logging.info(team_url)
            soup = BeautifulSoup(league_page, features="html.parser")
            table = soup.find('table')
            for player_section in table.find_all('tr'):
                player_attributes = []
                for player_attr_section in player_section.find_all('td'):
                    player_attributes.append(player_attr_section.text.strip())
                if not player_attributes[1] or player_attributes[0] == 'Number':
                    continue
                player = Player(
                    player_attributes[1], player_attributes[3], team_name, player_attributes[0])
                player.standardize_name()
                players.append(player)

        first_name_dict = get_first_name_dict([player.name for player in players])
        final_player_names = set()
        deduplicate_player_names(players, first_name_dict, final_player_names)
        with output_path.open("w") as f:
            f.write("Name,Position,Club,Number\n")
            for player in players:
                # print(player.to_csv_line(new_line=False))
                f.write(player.to_csv_line())

    def _get_team_url_dict(self, league_urls):
        team_url_dict = {}
        for league_url in league_urls:
            league_page = get_page(self._BASE_URL + league_url)
            soup = BeautifulSoup(league_page, features="html.parser")
            main = soup.find('div', attrs={'id': 'main'})
            for team_section in main.find_all('a'):
                team_name = team_section.text.replace(' ', '')
                team_url_dict[team_name] = team_section['href']
        return team_url_dict


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    maker = FootballSquadsSquadMaker()
    maker.get_squad(['national/worldcup/wc2022.htm'], EXPORT_PATH / 'WC2022.csv')
