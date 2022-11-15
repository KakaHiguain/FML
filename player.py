#!/usr/bin/env python3

import logging

from player_name_utils import remove_special_char, without_irregular_char


class Player:
    def __init__(self, name, position, club, number):
        self.name = remove_special_char(name)
        if not without_irregular_char(self.name):
            logging.error(f"{self.name} has irregular char.")
        self.club = remove_special_char(club)
        if not without_irregular_char(self.club):
            logging.error(f"{self.club} has irregular char.")
        self.number = int(number) if number else -1
        self.position = position

    def to_csv_line(self, new_line=True):
        line = f'{self.name},{self.position},{self.club},{self.number}'
        return line + '\n' if new_line else line

    def standardize_name(self):
        name_parts = [part for part in self.name.split(' ') if part != 'Junior']
        while len(name_parts) >= 2:
            last_second_part = name_parts[-2]
            if len(last_second_part) >= 4 or \
               (len(last_second_part) == 3 and last_second_part[0].isupper()):
                break
            name_parts[-2] += name_parts[-1]
            name_parts.pop()
        self.name = ' '.join(name_parts)