#!/usr/bin/env python3
# -*- coding:Windows-1252 -*-

from player import Player
from transfermarkt_club_name_map import STANDARD_CLUB_NAMES


# TODO: Need refactor to support more general player.
class TMPlayer(Player):
    def __init__(self, name, position, club, number, unique_id):
        super().__init__(name, position, club, number)
        self.unique_id = int(unique_id)
        self._standardize_club_name()

    def _standardize_club_name(self):
        club_words = self.club.split(' ')

        def is_valid_parts(word: str):
            if all([letter.isupper() for letter in word]):
                return False
            if word in ('CF', 'FC', 'Club', 'AFC'):
                return False
            return not any([letter.isdigit() for letter in word])
        self.club = ''.join(filter(is_valid_parts, club_words))

        if self.club in STANDARD_CLUB_NAMES:
            self.club = STANDARD_CLUB_NAMES[self.club]

    def to_csv_line(self, new_line=True):
        line = f'{self.name},{self.position},{self.club},{self.number},{self.unique_id}'
        return line + '\n' if new_line else line
