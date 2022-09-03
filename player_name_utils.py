#!/usr/bin/env python3
# -*- coding:utf-8 -*-


# To resolve duplicated player names.
HARECODED_PLAYER_NAMES = {
    44352: 'L.A.Suarez',
    424784: 'L.J.Suarez',
    129129: 'J.PedroGeraldino',
    607854: 'E.Silva',
    626724: 'J.PedroJunqueira',
    # FMC
    537602: 'J.MarioNeto',
    149729: 'J.MarioNaval',
    426723: 'M.A.Camara',
    520662: 'C.Pepe',
    14132: 'F.Pepe',
}


def remove_special_char(s):
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