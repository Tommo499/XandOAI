from math import sqrt, log, e
import random as r
import json
import os

datafolderprefix = os.path.dirname(os.path.realpath(__file__)) + '\\XandOdata*.json'  # use this if the data is in the
#                                                                                     same directory as this file
first = None
prettyboard = f" 7 ███ 8 ███ 9\n" \
              f"███████████████\n" \
              f" 4 ███ 5 ███ 6\n" \
              f"███████████████\n" \
              f" 1 ███ 2 ███ 3\n"

# constants for value algorithm
c = sqrt(2)
simulations = 1

winconditions = ('123', '456', '789', '147', '258', '369', '159', '357')


def fullycontained(sub: str, container: str):
    for item in sub:
        if item not in container:
            return False
    return True


def fetchjson(j):  # converts json string to dictionary
    import json
    temp1 = json.load(j)
    return_val = dict()
    for item in temp1:
        _ = list(eval(item))
        return_val[_[0]] = eval(item)[_[0]]
    return return_val


def fetchfromfile(filename: str):  # converts file with json string to dictionary
    with open(filename) as file:
        return_value = fetchjson(file)
    return return_value


def fetchfromdata(number: str):
    with open(datafolderprefix.replace('*', number)) as file:
        return_value = fetchjson(file)
    return return_value


def findchildren(parentname: str):
    children = []
    for potential_child in range(1, 10):
        if str(potential_child) not in parentname:
            children.append(parentname + str(potential_child))
    return children


def getdata(node: str):
    return fetchfromfile(datafolderprefix.replace('*', str(len(node))))[node]


def getchilddata(parent: str):
    child_file = fetchfromfile(datafolderprefix.replace('*', str(len(parent) + 1)))
    return_dict = dict()
    for child in child_file:
        if child.startswith(parent):
            return_dict[child] = child_file[child]
    return return_dict


def keyswithtopvalues(mydict: dict):
    return [key for (key, value) in mydict.items() if value == max(mydict.values())]


def choosechild(parent: str):
    roundnum = len(parent) + 1
    boarddata = fetchfromfile(datafolderprefix.replace('*', str(roundnum)))
    winratio = 0

    choicelist = dict()

    for child in findchildren(parent):
        data = getdata(child)
        wins = data['w']
        plays = data['p']
        templog = 0
        parentvisits = 0
        if parent == '':  # if the parent is blank, use the number of simulations
            parentvisits = json.load(open(os.path.dirname(os.path.realpath(__file__)) + "\\extra.json"))['simulations']
        else:
            parentvisits = getdata(parent)['p']
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
    returnvalue = ''
    if bot:
        returnvalue = choosechild(board_state)
    else:
        turn = input('>>> ')
        if verifyturn(turn, board_state):
            returnvalue = board_state + turn
        else:
            haveturn(board_state, bot)

    return returnvalue


def playsimulation():
    global first, prettyboard
    first = r.choice([False, True])  # True for the bot, false for humans
    playerpieces = {''}  # work out if which player is x or o
    if first:
        print('You are O')
    else:
        print('You are X')
    game = ''
    won = ''
    print(prettyboard)
    while won == '' and len(game) < 9:
        game = haveturn(game, first)
        first = not first  # can be removed for zero or two player game

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
        print(prettyboard)

    if won != '':
        print(f'Player {won} won')
    else:
        print('Tie')

    # update(game)


def verifyturn(turn: str, state: str):
    if turn.isdigit() and len(str(turn)) == 1:
        if turn not in state:
            return True
    return False


def update(endgame: str):
    botplays = []
    for l in range(1, len(endgame) + 1, 2):
        if (l + (not first)) <= len(endgame):
            botplays.append(endgame[0:l + (not first)])

    """
    for slices in range(1 + (not first), len(endgame) + 1, 2):
        wholefile = fetchfromdata(slices)
        
        wholefile[endgame[:slices]]['p'] += 1
"""


playsimulation()
quit()
