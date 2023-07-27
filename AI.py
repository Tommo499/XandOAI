# Thomas Wachmer 2022
import random as r
import sqlite3
from itertools import zip_longest
from math import sqrt, log, e, ceil, floor

con = sqlite3.connect('data.db')
cur = con.cursor()

first = None
game = ''
board1d = ''
# constants for value formula
c = sqrt(2)


winconditions = ('123', '456', '789', '147', '258', '369', '159', '357')


def sewstrings(str1, str2):
    return "".join(i + j for i, j in zip_longest(str1, str2, fillvalue=''))


class vector2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):
        if type(other) == int:
            return self.x * other, self.y * other
        elif type(other) == list:
            assert len(other) == 2
            return self.x * other[0], self.y * other[1]

    def __add__(self, other):
        assert len(other) == 2
        return self.x + other[0], self.y + other[1]

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __int__(self):  # Returns int corresponding to its position in a 1d array
        return self.x + self.y * 3

def replacecharindex(string, replace, index):
    l = list(string)
    l[index] = replace
    return ''.join(l)


def dbname(regularname):
    """
    Returns the name of the position as it is stored in the database
    Multiple regularnames can be converted to the same dbname by losing the order they were played
    """
    p1 = ''.join(sorted(list(regularname[0::2])))
    p2 = ''.join(sorted(list(regularname[1::2])))
    return p1 + p2


def regularname(dbname):
    """
    Returns a string showing a possible history of a game, alternating between p1 and p2
    """
    p1 = ''.join(sorted(list(dbname[0:ceil(len(dbname) / 2)])))
    p2 = ''.join(sorted(list(dbname[ceil(len(dbname) / 2):])))
    return sewstrings(p1, p2)


def sortregularname(name):
    """
    Converts a regularname to a dbname, then back again
    Returns a string where each player's moves are sorted by number
    """
    p1 = ''.join(sorted(list(str(name)[0::2])))
    p2 = ''.join(sorted(list(str(name)[1::2])))
    return sewstrings(p1, p2)


def fullycontained(sub: str, container: str):
    for item in sub:
        if item not in container:
            return False
    return True


def findchildren(parentname: str):
    """
    Finds possible child nodes from the current position
    """
    children = []
    for potential_child in range(1, 10):
        if str(potential_child) not in parentname:
            children.append(parentname + str(potential_child))
    return children


def getdata(node: str):
    cur.execute("SELECT * FROM data WHERE name = ?", (dbname(node),))
    return cur.fetchone()

# Finds the total number of simulations the data has done
simulations = 0
for _ in range(1, 10):
    simulations += getdata(str(_))[2]

def getchilddata(parent: str):
    child_file = []
    for i in range(1, 10):
        if i not in parent:
            child_file.append(parent + str(i))

    return_dict = child_file
    return return_dict


def keyswithtopvalues(mydict: dict):  # Probably from StackOverflow
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
            parentvisits = getdata(parent)[2] + 1
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


def gamewon(state: str):
    global board1d
    if len(state) < 5:
        return False, 0
    op = state[-1]  # The last move that has been played
    op2d = vector2d((int(int(op) - 1) % 3), floor((int(op) / 3) - 0.1)) # lets me work in 2 dimensions

    board1d = '-' * 9
    row = 3
    length = 1
    player1 = ''.join(sorted(list(state[0::2])))
    player1 = player1.replace('-', '')
    player2 = ''.join(sorted(list(state[1::2])))
    player2 = player2.replace('-', '')
    directions = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i, j) != (0, 0):
                if 0 <= op2d.x + i * length <= 2 and 0 <= op2d.y + j * length <= 2:
                    directions.append((i, j))

    for item in player1:
        board1d = replacecharindex(board1d, 'X', int(item) - 1)
    for item in player2:
        board1d = replacecharindex(board1d, 'O', int(item) - 1)

    matches = str(op)
    for direc in directions:
        length = 1
        adjustedposition = int(op2d) + length * (direc[0] + direc[1] * row)
        assert 0 <= adjustedposition <= 10
        while length < 3 and board1d[adjustedposition] == board1d[int(op2d)]:
            adjustedposition = op2d.x + direc[0] * length + (op2d.y + direc[1] * length) * row
            assert 0 <= adjustedposition <= 10
            assert 0 <= int(op2d) - 1 <= 10
            length += 1
            if board1d[adjustedposition] == board1d[int(op2d) - 1]:
                matches += str(adjustedposition + 1)

    sorted(matches)
    print(matches, op)

    for k in winconditions:
        i = True
        piece = board1d[int(op) - 1]
        for c in k:
            if board1d[int(c) - 1] != piece:
                i = False
                break
        if i:
            return True, op

    return False, op


def playsimulation(training: bool):
    global first, game
    prettyboard = f" 7 ███ 8 ███ 9\n" \
                  f"███████████████\n" \
                  f" 4 ███ 5 ███ 6\n" \
                  f"███████████████\n" \
                  f" 1 ███ 2 ███ 3\n"
    if training:
        first = True
    else:
        first = r.choice([True, False])  # True for the bot, false for humans
        print(prettyboard)

    game = ''

    if first and not training:
        print('You are O')
    elif not first and not training:
        print('You are X')

    won = 0
    while won == 0 and len(game) < 9:

        game = haveturn(game, first)

        player1 = ''.join(sorted(list(game[0::2])))
        player2 = ''.join(sorted(list(game[1::2])))

        for spot in player1:
            prettyboard = prettyboard.replace(spot, 'X')
        for spot in player2:
            prettyboard = prettyboard.replace(spot, 'O')

        if not training:
            first = not first  # can be removed for zero or two player game
            print(prettyboard)

        for cond in winconditions:
            if fullycontained(cond, player1):
                won = '1'
            elif fullycontained(cond, player2):
                won = '2'

    return won, game


def playgame():
    result = playsimulation(False)
    if result[0] != 0:
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
