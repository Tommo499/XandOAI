from itertools import permutations
import json
import math

winConditions = ('123', '456', '789', '147', '258', '369', '159', '357')
# ↑ will be useful to make the redundancy checker


def fully_contained(sub, container):
    for item in sub:
        if not item in container:
            return False
    return True


def redundant(game):  # checks if the game could have been ended earlier, only for games that have 6 rounds played
    if len(game) >= 6:
        for segment in range(5, len(game) + 1):
            partgame = game[:segment]
            player1 = ''.join(sorted(list(partgame[0::2])))
            player2 = ''.join(sorted(list(partgame[1::2])))
            for item in winConditions:
                if fully_contained(item, player1) and segment < len(game):
                    return True
                elif fully_contained(item, player2) and segment < len(game):
                    return True
    return False


spots = '123456789'
jsonList = []

""" When uncommenting, replace the file path with your file path
for leng in range(1,10):
    jsonList = []
    for branch in permutations(spots, leng):
        if not redundant(branch):
            temp = {''.join(branch): {'w': 0, 'p': 0}}
            jsonList.append(json.dumps(temp))
            del temp
    json.dump(jsonList, open(f"C:\\Users\\Thomas\\Documents\\XandOdata{leng}.json", 'w'))
    del jsonList


temp = {'simulations': 1, "c": math.sqrt(2)}
"""
