#!/usr/bin/env python3

from player_name_utils import remove_special_char


class Player:
    def __init__(self, name, position, club, number):
        self.name = remove_special_char(name)
        self.club = remove_special_char(club)
        self.number = int(number) if number else -1
        self.position = position
