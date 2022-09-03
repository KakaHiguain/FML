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
