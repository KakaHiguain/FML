#!/usr/bin/env python3

import csv
import re
from typing import List, Dict, Set

from common import *
from player import Player
from player_name_utils import get_unique_player_name, get_first_name_dict
from transfermarkt_club_name_utils import HARECODED_PLAYER_NAMES
from transfermarkt_player import TMPlayer


class FSPlayer(Player):
    def __init__(self, name, position, club, number):
        number = int(float(number)) if number else None
        super().__init__(name, position, club, number)


class PlayerDataBase:
    def __init__(self, player_list: List[Player]):
        self.dict = {}
        self._setup(player_list)

    def _setup(self, player_list: List[Player]):
        for player in player_list:
            key = (player.club, player.number)
            self.dict[key] = player

    def get(self, club: str, number: str) -> Player:
        return self.dict.get((club, number), None)


def read_player_csv(csv_file: Path, player_type: type) -> List[Player]:
    player_list = []
    with csv_file.open('r') as f:
        for row in csv.reader(f):
            if row[0] == 'Name':
                continue
            player_list.append(player_type(*row))

    return player_list


def merge_database(fs_player_database: PlayerDataBase,
                   tm_player_database: PlayerDataBase) -> List[TMPlayer]:
    player_list = []
    for (club, number), fs_player in fs_player_database.dict.items():
        assert club
        if not number:
            continue
        tm_player = tm_player_database.get(club, number)
        if tm_player:
            unique_id = tm_player.unique_id
        else:
            print('Cannot find transfermarkt player: club {}, number {}'.format(club, number))
            unique_id = -1
            continue
        fml_player = TMPlayer(tm_player.name, fs_player.position, club, number, unique_id)
        fml_player.standardize_name()
        player_list.append(fml_player)
    return player_list


def deduplicate_player_names(
        player_list: List[TMPlayer], first_name_dict: Dict[str, List[str]], final_player_names: Set[str]):
    for player in player_list:
        player.name = get_unique_player_name(player.name, first_name_dict)
        if player.unique_id in HARECODED_PLAYER_NAMES:
            player.name = HARECODED_PLAYER_NAMES[player.unique_id]
        if player.name in final_player_names:
            print('Still duplicate:', player.to_csv_line().rstrip())
        final_player_names.add(player.name)


def get_merged_player_list(fs_csv: Path, tm_csv: Path) -> List[TMPlayer]:
    fs_player_list = read_player_csv(fs_csv, FSPlayer)
    tm_player_list = read_player_csv(tm_csv, TMPlayer)
    fs_player_database = PlayerDataBase(fs_player_list)
    tm_player_database = PlayerDataBase(tm_player_list)

    fml_player_list = merge_database(fs_player_database, tm_player_database)
    return fml_player_list


def _export_to_csv(tournament: str, players: List[TMPlayer]):
    with (EXPORT_PATH / f"{tournament}squad.csv").open("w") as f:
        f.write("Name,Position,Club,Number,Unique ID\n")
        for player in players:
            if not re.match(r"^[A-Za-z'.\-]+$", player.name):
                print("Detect non-alphabet character in: ", player.name)
            f.write(player.to_csv_line())
            # print(player.to_csv_line().rstrip())


def main():
    fml_players = get_merged_player_list(
        EXPORT_PATH / f'FMLplayers{SEASON}.csv', EXPORT_PATH / 'tmsquad-FML.csv')
    fmc_players = get_merged_player_list(
        EXPORT_PATH / f'FMCplayers{SEASON}.csv', EXPORT_PATH / 'tmsquad-FMC.csv')

    first_name_dict = get_first_name_dict([player.name for player in fml_players + fmc_players])
    final_player_names = set()
    deduplicate_player_names(fml_players, first_name_dict, final_player_names)
    deduplicate_player_names(fmc_players, first_name_dict, final_player_names)

    _export_to_csv('FML', fml_players)
    _export_to_csv('FMC', fmc_players)


if __name__ == '__main__':
    main()
