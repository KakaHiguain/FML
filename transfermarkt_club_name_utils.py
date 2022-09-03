#!/usr/bin/env python3
# -*- coding:Windows-1252 -*-


STANDARD_CLUB_NAMES = {
    # TM club name -> standard club name
    # Spain
    'AtleticodeMadrid': 'AtleticoMadrid',
    'EspanyolBarcelona': 'Espanyol',
    'RealBetisBalompie': 'Betis',
    'CeltadeVigo': 'Celta',
    'RealValladolid': 'Valladolid',
    'RayoVallecano': 'Vallecano',
    'DeportivoAlaves': 'Alaves',

    # England
    'Brighton&HoveAlbion': 'Brighton',
    'SheffUtd': 'Sheffield',
    'Spurs': 'Tottenham',
    'LeedsUnited': 'Leeds',
    'LeicesterCity': 'Leicester',
    'NewcastleUnited': 'Newcastle',
    'ManchesterUnited': 'ManUtd',
    'ManchesterCity': 'ManCity',
    'NorwichCity': 'Norwich',
    'TottenhamHotspur': 'Tottenham',
    'WestHamUnited': 'WestHam',
    'WolverhamptonWanderers': 'Wolves',
    'NottinghamForest': "N'Forest",

    # Germany
    'ArminiaBielefeld': 'Bielefeld',
    'VfLBochum': 'Bochum',
    'BayerLeverkusen': 'Leverkusen',
    'BorussiaDortmund': 'Dortmund',
    "BorussiaMonchengladbach": "M'gladbach",
    'EintrachtFrankfurt': 'Frankfurt',
    'SpVggGreutherFurth': 'Furth',
    'Hertha': 'HerthaBerlin',
    'VfBStuttgart': 'Stuttgart',
    'WerderBremen': 'Bremen',
    'VfLWolfsburg': 'Wolfsburg',
    'SVWerderBremen': 'Bremen',

    # Italy
    'InterMilan': 'Inter',
    'CagliariCalcio': 'Cagliari',
    'SpeziaCalcio': 'Spezia',
    'UdineseCalcio': 'Udinese',
    'HellasVerona': 'Verona',

    # FMC
    # Portugal
    'Sporting': 'SportingCP',
    # France
    'ParisSaint-Germain': 'Paris',
    'OlympiqueMarseille': 'Marseille',
    'StadeRennais': 'Rennes',
    # Russia
    'LokoMoscow': 'LokomotivMoscow',
    'ZenitSt.Petersburg': 'Zenit',
    # Others
    'RedBullSalzburg': 'Salzburg',
    'Olympiacos': 'Olympiakos',
    'Basaksehir': 'Istanbul',
    'ShakhtarDonetsk': 'Shakhtar',
    'AjaxAmsterdam': 'Ajax',
    'Copenhagen': 'Kobenhavn',
}


def standardize_club_name(club) -> str:
    club_words = club.split(' ')

    def is_valid_parts(word: str):
        if all([letter.isupper() for letter in word]):
            return False
        if word in ('CF', 'FC', 'Club', 'AFC'):
            return False
        return not any([letter.isdigit() for letter in word])

    trimmed_club = ''.join(filter(is_valid_parts, club_words))
    return STANDARD_CLUB_NAMES.get(trimmed_club, trimmed_club)