from math import sqrt, log, e
import random as r
import json


datafolderprefix = "C:\\Users\\Thomas\\Documents\\XandOdata*.json"  # The asterisk gets replaced with the file number
first = None
prettyboard = f" 7 ███ 8 ███ 9\n" \
        f"███████████████\n" \
        f" 4 ███ 5 ███ 6\n" \
        f"███████████████\n" \
        f" 1 ███ 2 ███ 3\n"

# constants for value algorithm
c = sqrt(2)
simulations = 1

winConditions = ('123', '456', '789', '147', '258', '369', '159', '357')

def fully_contained(sub: str, container: str):
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
    with open(f"C:\\Users\\Thomas\\Documents\\XandOdata{number}.json") as file:
        return_value = fetchjson(file)
    return return_value

def find_children(parentname: str):
    children = []
    for potential_child in range(1, 10):
        if str(potential_child) not in parentname:
            children.append(parentname + str(potential_child))
    return children

def getdata(node: str):
    return fetchfromfile(datafolderprefix.replace('*', str(len(node))))[node]

def getchilddata(parent: str):
    child_file = fetchfromfile(datafolderprefix.replace('*', str(len(parent)+1)))
    return_dict = dict()
    for child in child_file:
        if child.startswith(parent):
            return_dict[child] = child_file[child]
    return return_dict

def keys_with_top_values(my_dict: dict):
    return [key for (key, value) in my_dict.items() if value == max(my_dict.values())]

def choose_child(parent: str):
    roundnum = len(parent) + 1
    boarddata = fetchfromfile(datafolderprefix.replace('*', str(roundnum)))
    win_ratio = 0

    choice_list = dict()

    for child in find_children(parent):
        data = getdata(child)
        wins = data['w']
        plays = data['p']
        templog = 0
        parent_visits = 0
        if parent == '':  # if the parent is blank, use the number of simulations
            parent_visits = json.load(open("C:\\Users\\Thomas\\Documents\\extra.json"))['simulations']
        else:
            parent_visits = getdata(parent)['p']
        if plays == 0:  # sets the factor to 10 to guarentee every one is used at least once
            choice_factor = 10
        else:
            win_ratio = wins / plays
            templog = log(parent_visits, e)
            choice_factor = win_ratio + c * sqrt(templog/plays)
        choice_list[child] = choice_factor

    best_child = r.choice(keys_with_top_values(choice_list))

    return best_child

def have_turn(board_state: str, bot: bool):
    returnvalue = ''
    if bot:
        returnvalue = choose_child(board_state)
    else:
        turn = input('>>> ')
        if verify_turn(turn, board_state):
            returnvalue = board_state + turn
        else:
            have_turn(board_state, bot)

    return returnvalue

def play_simulation():
    global first, prettyboard
    first = r.choice([True, True])  # True if the bot is first, false otherwise
    playerpieces = {''}  # work out if which player is x or o
    if first:
        print('You are O')
    else:
        print('You are X')
    game = ''
    won = ''
    player1 = ''.join(sorted(list(game[0::2])))
    player2 = ''.join(sorted(list(game[1::2])))
    while won == '' and len(game) < 9:
        game = have_turn(game, first)
        #first = not first

        player1 = ''.join(sorted(list(game[0::2])))
        player2 = ''.join(sorted(list(game[1::2])))
        for item in winConditions:
            if fully_contained(item, player1):
                won = 1
            elif fully_contained(item, player2):
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

    update(game)

def verify_turn(turn: str, state: str):
    if turn in state:
        return False
    return True

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


play_simulation()
quit()
