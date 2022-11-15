#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from collections import defaultdict
import re
from typing import Dict, List


def without_irregular_char(s: str) -> bool:
    return bool(re.match(r"^[\sa-zA-Z'.-]+$", s))


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


def remove_special_char(s):
    s = s.replace(' ', ' ')
    # special
    s = s.replace('&#263;', 'c')
    # aA
    s = s.replace('á', 'a')
    s = s.replace('ã', 'a')
    s = s.replace('ä', 'a')
    s = s.replace('à', 'a')
    s = s.replace('å', "aa")
    s = s.replace('ą', 'a')
    s = s.replace('â', 'a')
    s = s.replace('ă', 'a')
    s = s.replace('æ', 'ae')
    s = s.replace('Á', 'A')
    # oO
    s = s.replace('ö', 'o')
    s = s.replace('ó', 'o')
    s = s.replace('Ö', 'O')
    s = s.replace('ø', 'o')
    s = s.replace('Ó', 'O')
    s = s.replace('ô', 'o')
    s = s.replace('ð', 'o')
    s = s.replace('ō', 'o')
    s = s.replace('ò', 'o')
    s = s.replace('Ø', 'O')
    # eE
    s = s.replace('ë', 'e')
    s = s.replace('é', 'e')
    s = s.replace('è', 'e')
    s = s.replace('ę', 'e')
    s = s.replace('ě', 'e')
    s = s.replace('ê', 'e')
    s = s.replace('È', 'E')
    s = s.replace('É', 'E')
    # i
    s = s.replace('í', 'i')
    s = s.replace('ï', 'i')
    s = s.replace('ı', 'i')
    s = s.replace('İ', 'I')
    s = s.replace('Í', 'I')
    # uU
    s = s.replace('ü', 'u')
    s = s.replace('ú', 'u')
    s = s.replace('ů', 'u')
    s = s.replace('Ü', 'U')
    # consonants
    s = s.replace('Ď', 'D')
    s = s.replace('ñ', 'n')
    s = s.replace('ń', 'n')
    s = s.replace('Ñ', 'N')
    s = s.replace('ß', 'ss')
    s = s.replace('ś', 's')
    s = s.replace('š', 's')
    s = s.replace('ş', 's')
    s = s.replace('ș', 's')
    s = s.replace('Š', 'S')
    s = s.replace('Ś', 'S')
    s = s.replace('ç', 'c')
    s = s.replace('č', 'c')
    s = s.replace('ć', 'c')
    s = s.replace('Ç', 'C')
    s = s.replace('Ć', 'C')
    s = s.replace('Č', 'C')
    s = s.replace('ý', 'y')
    s = s.replace('ž', 'z')
    s = s.replace('ź', 'z')
    s = s.replace('Ż', 'Z')
    s = s.replace('Ž', 'Z')
    s = s.replace('ğ', 'g')
    s = s.replace('Ł', 'L')
    s = s.replace('Ľ', 'L')
    s = s.replace('ł', 'l')
    s = s.replace('ř', 'r')
    s = s.replace('ţ', 't')
    s = s.strip()
    return s