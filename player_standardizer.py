#!/usr/bin/env python3
import re

from FML_squad_maker_main import standardize_player_names
from transfermarkt_squad_maker import TMPlayer


player_list = []
with open('squads.csv') as f:
    lines = f.readlines()
for line in lines[1:]:
    _, _, name, pos, nat, number, _ = line.split(',')
    player_list.append(TMPlayer(name, pos, nat, number, 0))

standardize_player_names(player_list)

with open('FME-2021Squad.csv', "w") as export_csv:
    export_csv.write("Order,Price,Name,Position,Team,Number\n")
    for player in player_list:
        export_csv.write(',,' + player.to_csv_line())
        print(player.to_csv_line())
        # if not re.match(r"^[A-Za-z'.\-]+$", player.name):
        #     print(player.name)