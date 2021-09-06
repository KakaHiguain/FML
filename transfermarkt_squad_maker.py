#!/usr/bin/env python3
# -*- coding:Windows-1252 -*-

import re
from typing import List

from bs4 import BeautifulSoup

from common import *
from crawler import get_page
from player import Player
from player_name_utils import remove_special_char

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'cookie': 's_ga=GA1.2.974713430.1556589812; __gads=ID=2f635078c6e37fc5:T=1556589814:S=ALNI_MYBlZckdQFx6vD8iADC_aclVRvw-Q; TMSESSID=1jg57ttfian37t5q6loalfu066; _gid=GA1.2.792961174.1564539337; POPUPCHECK=1564625920497; ioam2018=001a4fbfad5e90b375cc7acf2:1584324212713:1556589812713:.transfermarkt.com:112:transfer:ausland_rest_r:noevent:1564565972027:i5qaft; utag_main=v_id:016a6bfb9b8e0022bbb662e25bb803069001e06100bd0$_sn:9$_ss:0$_st:1564567768238$dc_visit_transfermarkt-transfermarkt.de:7$dip_visitor_id:016a6bfbb144001aa0b25bd0ac8b03069001e06100bd0$dc_visit_dip-main:8$ses_id:1564564905485%3Bexp-session$_pn:4%3Bexp-session$collectCookieMode:3rdParty%3Bexp-session$dc_event_transfermarkt-transfermarkt.de:3%3Bexp-session$dip_events_this_session:4%3Bexp-session$dc_event_dip-main:4%3Bexp-session$dc_region_transfermarkt-transfermarkt.de:eu-central-1%3Bexp-session$dc_region_dip-main:eu-central-1%3Bexp-session'
}

BASE_URL = "https://www.transfermarkt.com"

TOP4_LEAGUE = {"Laliga": "ES1", "Premier League": "GB1", "Bundesliga": "L1", "Seria A": "IT1"}


# TODO: Need refactor to support more general player.
class TMPlayer(Player):
    _STANDARD_CLUB_NAMES = {
        'SheffUtd': 'Sheffield',
        'Spurs': 'Tottenham',
        'Athletic': 'AthleticBilbao',
        'FCBarcelona': 'Barcelona',
        'RealBetis': 'Betis',
        'CadizCF': 'Cadiz',
        'CeltadeVigo': 'Celta',
        'SDEibar': 'Eibar',
        'ElcheCF': 'Elche',
        'GranadaCF': 'Granada',
        'SDHuesca': 'Huesca',
        'CAOsasuna': 'Osasuna',
        'SevillaFC': 'Sevilla',
        'RealValladolid': 'Valladolid',
        'RayoVallecano': 'Vallecano',
        'RCDMallorca': 'Mallorca',
        'FCBayern': 'BayernMunich',
        'Arm.Bielefeld': 'Bielefeld',
        'VfLBochum': 'Bochum',
        'FCAugsburg': 'Augsburg',
        'Bay.Leverkusen': 'Leverkusen',
        'Bor.Dortmund': 'Dortmund',
        "Bor.M'gladbach": "M'gladbach",
        'E.Frankfurt': 'Frankfurt',
        'SCFreiburg': 'Freiburg',
        'GreutherFurth': 'Furth',
        'HerthaBSC': 'HerthaBerlin',
        'TSGHoffenheim': 'Hoffenheim',
        '1.FCKoln': 'Koln',
        'RBLeipzig': 'Leipzig',
        '1.FSVMainz05': 'Mainz',
        'FCSchalke04': 'Schalke',
        'VfBStuttgart': 'Stuttgart',
        'WerderBremen': 'Bremen',
        'VfLWolfsburg': 'Wolfsburg',
        'CagliariCalcio': 'Cagliari',
        'ACMilan': 'Milan',
        'SSCNapoli': 'Napoli',
        'ASRoma': 'Roma',
        'SpeziaCalcio': 'Spezia',
        'UdineseCalcio': 'Udinese',
        'HellasVerona': 'Verona',
        'AtalantaBC': 'Atalanta',
        'FCEmpoli': 'Empoli',
        # FMC
        'LokoMoscow': 'LokomotivMoscow',
        'RBSalzburg': 'Salzburg',
        'ShakhtarD.': 'ShakhtarDonetsk',
        'Olympiacos': 'Olympiakos',
        'FCPorto': 'Porto',
        'FCMidtjylland': 'Midtjylland',
        'StadeRennais': 'Rennes',
        'ClubBrugge': 'Brugge',
        'ZenitS-Pb': 'Zenit',
        'Basaksehir': 'Istanbul',
        'ParisSG': 'Paris',
        'BSCYoungBoys': 'YoungBoys',
        'LOSCLille': 'Lille',
        'MalmoFF': 'Malmo',
        'FCSheriff': 'Sheriff',
        'ShakhtarDonetsk': 'Shakhtar',
    }

    def __init__(self, name, position, club, number, unique_id):
        super().__init__(name, position, club, number)
        self.unique_id = int(unique_id)
        self._standardize_club_name()

    def _standardize_club_name(self):
        if self.club in self._STANDARD_CLUB_NAMES:
            self.club = self._STANDARD_CLUB_NAMES[self.club]

    def to_csv_line(self):
        return '{},{},{},{},{}\n'.format(
            self.name, self.position, self.club, self.number, self.unique_id)


def get_club_urls(league_page):
    res = []
    club_url_regex = r'<a class="vereinprofil_tooltip" id="\d*" href="([^"]*)">([^<]*)</a></td>'
    for m in re.compile(club_url_regex).finditer(league_page):
        res.append([m.group(2), BASE_URL + m.group(1)])
    return res


def get_players(club: List[str]) -> List[TMPlayer]:
    club_name = club[0]
    print("Visit:", club[0], club[1])
    club_page = get_page(club[1], HEADERS)
    club_page_part = club_page[club_page.find('<div class="responsive-table">'):
                               club_page.find('<div class="table-footer">')]
    soup = BeautifulSoup(club_page_part, features="html.parser")

    player_table = soup.find('table', attrs={'class': 'items'}).find('tbody')
    player_list = []
    for item in player_table.find_all('tr', recursive=False):
        player_attrs = item.find_all('td', recursive=False)
        # <td class="zentriert rueckennummer bg_Torwart" title="Goalkeeper">
        #   <div class="rn_nummer">1</div>
        # </td>
        position = player_attrs[0]['title'][0].upper()
        number = player_attrs[0].find('div').text
        if not number.isdigit():
            continue

        # <a class="spielprofil_tooltip tooltipstered" id="74857"
        #  href="/marc-andre-ter-stegen/profil/spieler/74857">M. ter Stegen</a>
        player_item = player_attrs[1].find('a', attrs={'class': 'spielprofil_tooltip'})
        name = player_item.text
        unique_id = player_item['id']

        if position == 'A':
            position = 'F'
        new_player = TMPlayer(name, position, club_name, number, unique_id)
        player_list.append(new_player)
        print(new_player.to_csv_line())

    # Count the detail position (like LW, RW, AM, etc), Deprecated.
    #
    # club_page = club_page[club_page.find('itemprop="athlete"'):club_page.rfind('itemprop="athlete"') + 60]
    # player_regex = r'<td>([^<]*)</td></tr></table></td><td class="hide" itemprop="athlete">([^<]*)</td>'
    # for m in re.compile(player_regex).finditer(club_page):
    #     position = m.group(1)
    #     name = remove_special_char(m.group(2))
    #     print(name, position)
    #     player_list.append(TMPlayer(name, position, players[name][0], players[name][1], players[name][2]))
    #     if position not in POSITION_COUNT:
    #         POSITION_COUNT[position] = 0
    #     POSITION_COUNT[position] += 1
    return player_list


# Main =============================================
def get_fml_squad():
    league_base_url = BASE_URL + "/jumplist/startseite/wettbewerb/"

    csv_file = EXPORT_PATH / 'tmsquad-FML.csv'
    with csv_file.open("w") as f:
        f.write("Name,Position,Club,Number,Unique ID\n")
        for league_name, league_suffix in TOP4_LEAGUE.items():
            league_url = league_base_url + league_suffix
            print("Visit:", league_name, league_url)
            league_page = get_page(league_url, HEADERS)
            clubs = get_club_urls(league_page)

            for club in clubs:
                club[0] = remove_special_char(club[0])
                for player in get_players(club):
                    f.write(player.to_csv_line())


def read_ucl_page() -> List[List[str]]:
    UCL_URL = 'https://www.transfermarkt.com/champions-league/startseite/pokalwettbewerb/CL'
    ucl_page = get_page(UCL_URL, HEADERS)
    ucl_page_2 = ucl_page[ucl_page.find('<div class="table-header">Group table'):]
    soup = BeautifulSoup(ucl_page_2, features="html.parser")
    clubs = []
    for group in soup.find_all('a', attrs={'class': 'vereinprofil_tooltip'}):
        if not group.text:
            continue
        # Hack...
        club_url = str(group['href']).replace('spielplan', 'startseite')
        club = [str(group.text), BASE_URL + club_url]
        print(club)
        clubs.append(club)
    return clubs


def get_fmc_squad():
    csv_file = EXPORT_PATH / 'tmsquad-FMC.csv'
    with csv_file.open("w") as f:
        f.write("Name,Position,Club,Number,Unique ID\n")
        clubs = read_ucl_page()
        # clubs = [['Paris', 'https://www.transfermarkt.com/fc-paris-saint-germain/startseite/verein/583/saison_id/2020'],
        #          ['Porto', 'https://www.transfermarkt.com/fc-porto/startseite/verein/720/saison_id/2020']]
        for club in clubs:
            club[0] = remove_special_char(club[0])
            for player in get_players(club):
                f.write(player.to_csv_line())


if __name__ == '__main__':
    # pass
    # get_fml_squad()
    get_fmc_squad()
