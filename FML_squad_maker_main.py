#!/usr/bin/env python3

from collections import defaultdict
import csv
from pathlib import Path
import re
from typing import List, Dict

from common import *
from player import Player
from player_name_utils import HARECODED_PLAYER_NAMES
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


def get_unique_player_name(name: str, first_name_dict: Dict[str, List[str]]):
    name_parts = name.split(' ')
    if len(name_parts) == 1:
        return name
    last_name, first_name = name_parts[-1], name_parts[-2]
    first_names = first_name_dict[last_name]
    if len(first_names) == 1:
        return last_name
    first_letter = first_name[0]
    is_duplicated = False
    for name in first_names:
        if name and name != first_name and name[0] == first_letter:
            is_duplicated = True

    if not is_duplicated:
        return '{}.{}'.format(first_letter, last_name)
    return first_name + last_name


def get_first_name_dict(player_names: List[str]) -> Dict[str, List[str]]:
    """ Return last name -> list of first names """
    last_name_set = set()
    first_name_count = defaultdict(int)
    first_name_dict = defaultdict(list)
    for name in player_names:
        name_parts = name.split(' ')
        last_name = name_parts[-1]
        first_name = name_parts[-2] if len(name_parts) > 1 else ''
        last_name_set.add(last_name)
        first_name_count[first_name] += 1
        first_name_dict[last_name].append(first_name)
    return first_name_dict


def deduplicate_player_names(player_list: List[TMPlayer], first_name_dict: Dict[str, List[str]]):
    final_name_set = set()
    for player in player_list:
        player.name = get_unique_player_name(player.name, first_name_dict)
        if player.unique_id in HARECODED_PLAYER_NAMES:
            player.name = HARECODED_PLAYER_NAMES[player.unique_id]
        if player.name in final_name_set:
            print('Still duplicate:', player.to_csv_line().rstrip())
        final_name_set.add(player.name)


def get_merged_player_list(fs_csv: Path, tm_csv: Path) -> List[TMPlayer]:
    fs_player_list = read_player_csv(fs_csv, FSPlayer)
    tm_player_list = read_player_csv(tm_csv, TMPlayer)
    fs_player_database = PlayerDataBase(fs_player_list)
    tm_player_database = PlayerDataBase(tm_player_list)

    fml_player_list = merge_database(fs_player_database, tm_player_database)
    return fml_player_list


def main():
    fml_players = get_merged_player_list(
        EXPORT_PATH / f'FMLplayers{SEASON}.csv', EXPORT_PATH / 'tmsquad-FML.csv')
    fmc_players = get_merged_player_list(
        EXPORT_PATH / f'FMCplayers{SEASON}.csv', EXPORT_PATH / 'tmsquad-FMC.csv')

    first_name_dict = get_first_name_dict([player.name for player in fml_players + fmc_players])
    deduplicate_player_names(fml_players, first_name_dict)
    deduplicate_player_names(fmc_players, first_name_dict)
    with (EXPORT_PATH / "FMLsquad.csv").open("w") as f:
        f.write("Name,Position,Club,Number,Unique ID\n")
        for player in fml_players:
            # Detect non-alphabet character.
            if not re.match(r"^[A-Za-z'.\-]+$", player.name):
                print(player.name)
            f.write(player.to_csv_line())
            # print(player.to_csv_line().rstrip())
    with (EXPORT_PATH / "FMCsquad.csv").open("w") as f:
        f.write("Name,Position,Club,Number,Unique ID\n")
        for player in fmc_players:
            if not re.match(r"^[A-Za-z'.\-]+$", player.name):
                print(player.name)
            f.write(player.to_csv_line())


if __name__ == '__main__':
    main()
