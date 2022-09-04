#!/usr/bin/env python3
# -*- coding:Windows-1252 -*-

from player import Player


# TODO: Need refactor to support more general player.
class TMPlayer(Player):
    def __init__(self, name, position, club, number, unique_id):
        super().__init__(name, position, club, number)
        self.unique_id = int(unique_id)

    def to_csv_line(self, new_line=True):
        line = f'{self.name},{self.position},{self.club},{self.number},{self.unique_id}'
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
