import random as r
import sqlite3
from itertools import zip_longest
from math import sqrt, log, e, ceil


con = sqlite3.connect('data.db')
cur = con.cursor()

first = None
game = ''
# constants for value algorithm
c = sqrt(2)
simulations = 1

winconditions = ('123', '456', '789', '147', '258', '369', '159', '357')


def sewstrings(str1, str2):
    return "".join(i + j for i, j in zip_longest(str1, str2, fillvalue=''))


def dbname(regularname):
    p1 = ''.join(sorted(list(regularname[0::2])))
    p2 = ''.join(sorted(list(regularname[1::2])))
    return p1 + p2


def regularname(dbname):
    p1 = ''.join(sorted(list(dbname[0:ceil(len(dbname) / 2)])))
    p2 = ''.join(sorted(list(dbname[ceil(len(dbname) / 2):])))
    return sewstrings(p1, p2)


def sortregularname(name):
    p1 = ''.join(sorted(list(str(name)[0::2])))
    p2 = ''.join(sorted(list(str(name)[1::2])))
    return sewstrings(p1, p2)


def fullycontained(sub: str, container: str):
    for item in sub:
        if item not in container:
            return False
    return True


def findchildren(parentname: str):
    children = []
    for potential_child in range(1, 10):
        if str(potential_child) not in parentname:
            children.append(parentname + str(potential_child))
    return children


def getdata(node: str):
    cur.execute("SELECT * FROM data WHERE name = ?", (dbname(node),))
    return cur.fetchone()

def getchilddata(parent: str):
    child_file = []
    for i in range(1, 10):
        if i not in parent:
            child_file.append(parent + str(i))

    return_dict = dict()
    return return_dict


def keyswithtopvalues(mydict: dict):
    return [key for (key, value) in mydict.items() if value == max(mydict.values())]


def choosechild(parent: str):
    choicelist = dict()

    for child in findchildren(parent):
        data = getdata(child)
        wins = data[1]
        plays = data[2]
        if parent == '':  # if the parent is blank, use the number of simulations
            parentvisits = 10
        else:
            parentvisits = getdata(parent)[2]
        if plays == 0:  # sets the factor to 10 to guarentee every one is used at least once
            choicefactor = 10
        else:
            winratio = wins / plays
            templog = log(parentvisits, e)
            choicefactor = winratio + c * sqrt(templog / plays)
        choicelist[child] = choicefactor

    best_child = r.choice(keyswithtopvalues(choicelist))

    return best_child


def haveturn(board_state: str, bot: bool):
    if bot:
        returnvalue = choosechild(board_state)
    else:
        turn = input('>>> ')
        if verifyturn(turn, board_state):
            returnvalue = board_state + turn
        else:
            returnvalue = haveturn(board_state, bot)

    return returnvalue


def playsimulation():
    global first, game
    game = ''
    prettyboard = f" 7 ███ 8 ███ 9\n" \
                  f"███████████████\n" \
                  f" 4 ███ 5 ███ 6\n" \
                  f"███████████████\n" \
                  f" 1 ███ 2 ███ 3\n"
    first = r.choice([True])  # True for the bot, false for humans
    """
    if first:
        print('You are O')
    else:
        print('You are X')
    """
    won = 0
#    print(prettyboard)
    while won == 0 and len(game) < 9:

        game = haveturn(game, first)
#        first = not first  # can be removed for zero or two player game

        player1 = ''.join(sorted(list(game[0::2])))
        player2 = ''.join(sorted(list(game[1::2])))
        for item in winconditions:
            if fullycontained(item, player1):
                won = 1
            elif fullycontained(item, player2):
                won = 2
        for spot in player1:
            prettyboard = prettyboard.replace(spot, 'X')
        for spot in player2:
            prettyboard = prettyboard.replace(spot, 'O')
#        print(prettyboard) #  comment out for training
    return won, game


def playgame():
    result = playsimulation()
    if result != 0:
        print(f"Player {result[0]} won")
    else:
        print("Tie")


def verifyturn(turn: str, state: str):
    if turn.isdigit() and len(str(turn)) == 1:
        if turn not in state:
            return True
    return False


def sortgame(game: str):
    p1 = ''.join(sorted(list(game[0::2])))
    p2 = ''.join(sorted(list(game[1::2])))
    returnvalue = ''
    print(p1, p2)

    return returnvalue
