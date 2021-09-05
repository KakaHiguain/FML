# -*- coding:Windows-1252 -*-

import re
import os

from player_name_utils import remove_special_char


def getPage(url):
    file_object = open(url, "r")

    try:
        file_context = file_object.read()
        return file_context
    except e:
        pass
    finally:
        file_object.close()




Top4League = ("LaLiga", "Serie A", "Bundesliga", "Premier League")
FamousLastName = set([])
# FamousLastName = set(['Fernandez', 'Smith', 'Williams', 'Hernandez', \
#                       'Torres', 'Gomez', 'Lopez', 'Johnson', 'Silva', \
#                       'Davies', 'Wood', 'Costa', 'Rodriguez', 'Brown', \
#                       'Sanchez', 'Gonzalez', 'Garcia', 'Moreno', 'Martinez', 'Suarez'])
count = 0

squad_path = "SquadAmerica2019"
finalFile = open("America2019-Squad.csv", "w")
playerList = []
nameDict = {}
firstNameDict = {}
for file in os.listdir(squad_path):
    clubURL = os.path.join(squad_path, file)
    clubName = file.split(" - ")[1]
    count += 1
    print "[%s] (%d/12)" % (clubName, count)
    clubPage = getPage(clubURL).decode('Windows-1252')

    # end = str(clubPage.encode('utf-8')).index("Players no longer at this club")
    # clubPage = clubPage[:end]


    s = r'(\d+)</td>\s*<td.*>(.+)</td>\s*<td.*>[A-Z]+</td>\s*<td.*>(.+)</td>'
    # re for each player information
    p2 = re.compile(s)
    # playerList = []

    for m2 in p2.finditer(clubPage):  # Get the information for each player
        # print m2.group(0)
        fullName = remove_special_char(m2.group(2)).encode('utf-8')  # Modify their name to avoid special characters
        if len(fullName) == 0:
            continue
        number = int(m2.group(1).encode('utf-8'))
        position = m2.group(3).replace("</i>", "").encode('utf-8')
        if len(fullName) > 0:
            splitedName = fullName.split()
            lastName = splitedName[-1]
            Len = len(splitedName)

            if Len > 1:
                firstName = splitedName[-2]
                if lastName in FamousLastName:
                    playerList.append([clubName, number, firstName + lastName, position])
                else:
                    if (Len >= 3) and (len(firstName) <= 3):
                        playerList.append([clubName,number, firstName + lastName, position])
                        # print str(number),' ',firstName+lastName,' ',position
                    else:
                        firstChar = ord(firstName[0].upper()) - 65
                        playerList.append([clubName, number, firstName + "  " + lastName, position])
                        if not nameDict.has_key(lastName):
                            nameDict[lastName] = [0 for i in range(26)]
                        # print lastName,' ',firstChar
                        nameDict[lastName][firstChar] += 1
                        firstNameDict[firstName] = firstNameDict.get(firstName, 0) + 1

            else:
                playerList.append([clubName, number, fullName, position])
                firstNameDict[fullName] = firstNameDict.get(fullName, 0) + 1

for player in playerList:
    # print player[0], str(player[1]), player[2], player[3]
    name = player[2]
    if name.find("  ") >= 0:
        splitedName = name.split()
        lastName = splitedName[-1]
        firstName = splitedName[-2]
        if sum(nameDict[lastName]) == 1:
            player[2] = lastName
        else:
            firstChar = ord(firstName[0].upper()) - 65
            if nameDict[lastName][firstChar] == 1:
                player[2] = firstName[0] + "." + lastName
            else:
                if nameDict.has_key(firstName) or firstNameDict[firstName] > 1:
                    print player[2],
                    player[2] = firstName + lastName
                    print player[2]
                else:
                    print player[2],
                    player[2] = firstName
                    print player[2]

    finalFile.write(player[0] + ', ' + str(player[1]) + ', ' + player[2] + ', ' + player[3] + "\n")
finalFile.close()
