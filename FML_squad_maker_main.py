#!/usr/bin/env python3

from collections import defaultdict
import csv
from pathlib import Path
import re
from typing import List, Dict, Set

from common import *
from player import Player
from transfermarkt_squad_maker import TMPlayer


HARECODED_PLAYER_NAMES = {
    # 32816: 'Larangeira',
    # 476344: 'Aparecido',
    44352: 'L.A.Suarez',
    424784: 'L.J.Suarez',
    129129: 'J.PedroGeraldino',
    626724: 'J.PedroJunqueira',
    # 181768: 'Azevedo',
    # # FMC
    # 258018: 'P.Rodrigues',
    # 129473: 'R.Alcantara',
    537602: 'J.MarioNeto',
    149729: 'J.MarioNaval',
    426723: 'M.A.Camara',
    520662: 'Pepe(F)',
    14132: 'Pepe(D)',
}


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
        player_list.append(fml_player)
    return player_list


def get_unique_player_name(name: str, first_name_dict: Dict[str, List[str]],
                           last_name_set: Set[str], first_name_count: Dict[str, int]):
    name_parts = name.split(' ')
    if len(name_parts) == 1:
        return name
    last_name, first_name = name_parts[-1], name_parts[-2]
    first_names = first_name_dict[last_name]
    if len(first_names) == 1:
        return last_name
    # if first_name not in last_name_set and first_name_count[first_name] == 1:
    #     return first_name
    first_letter = first_name[0]
    is_duplicated = False
    for name in first_names:
        if name and name != first_name and name[0] == first_letter:
            is_duplicated = True

    if not is_duplicated:
        return '{}.{}'.format(first_letter, last_name)
    return first_name + last_name


def standardize_player_names(player_list: List[TMPlayer]):
    for player in player_list:
        name_parts = [part for part in player.name.split(' ') if part != 'Junior']
        while len(name_parts) >= 2:
            last_second_part = name_parts[-2]
            if len(last_second_part) >= 4 or \
               (len(last_second_part) == 3 and last_second_part[0].isupper()):
                break
            name_parts[-2] += name_parts[-1]
            name_parts.pop()
        player.name = ' '.join(name_parts)

    last_name_set = set()
    first_name_count = defaultdict(int)
    first_name_dict = defaultdict(list)
    for player in player_list:
        name_parts = player.name.split(' ')
        last_name = name_parts[-1]
        first_name = name_parts[-2] if len(name_parts) > 1 else ''
        last_name_set.add(last_name)
        first_name_count[first_name] += 1
        first_name_dict[last_name].append(first_name)

    final_name_set = set()
    for player in player_list:
        player.name = get_unique_player_name(player.name, first_name_dict, last_name_set, first_name_count)
        if player.unique_id in HARECODED_PLAYER_NAMES:
            player.name = HARECODED_PLAYER_NAMES[player.unique_id]
        if player.name in final_name_set:
            print('Duplicate:', player.to_csv_line().rstrip())
        final_name_set.add(player.name)


def main(fs_csv: Path, tm_csv: Path, output_csv: Path):
    fs_player_list = read_player_csv(fs_csv, FSPlayer)
    tm_player_list = read_player_csv(tm_csv, TMPlayer)
    fs_player_database = PlayerDataBase(fs_player_list)
    tm_player_database = PlayerDataBase(tm_player_list)

    fml_player_list = merge_database(fs_player_database, tm_player_database)

    standardize_player_names(fml_player_list)
    with output_csv.open("w") as f:
        f.write("Name,Position,Club,Number,Unique ID\n")
        for player in fml_player_list:
            # Detect non-alphabet character.
            if not re.match(r"^[A-Za-z'.\-]+$", player.name):
                print(player.name)
            f.write(player.to_csv_line())
            # print(player.to_csv_line().rstrip())


if __name__ == '__main__':
    for tournament in ['FML']:
        main(EXPORT_PATH / f'{tournament}players{SEASON}.csv',
             EXPORT_PATH / f'tmsquad-{tournament}.csv',
             EXPORT_PATH / f"{tournament}squad.csv")
