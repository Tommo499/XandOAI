from itertools import permutations
import math
import sqlite3 as sql
from AI import *

con = sql.connect('data.db')
cur = con.cursor()

winConditions = ('123', '456', '789', '147', '258', '369', '159', '357')
# ↑ useful to make the redundancy checker


def fully_contained(sub, container):
    for item in sub:
        if item not in container:
            return False
    return True


def redundant(game):  # checks if the game could have been ended earlier
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
writelist = []

for leng in range(1, 10):
    for branch in permutations(spots, leng):
        if not redundant(branch):
            p1 = ''.join(sorted(list(branch[0::2])))
            p2 = ''.join(sorted(list(branch[1::2])))
            temp = (p1 + p2, 0, 0)
            if temp not in writelist:
                writelist.append(temp)

cur.executemany("insert into data values (?, ?, ?)", writelist)

con.commit() # Save the changes to the file
