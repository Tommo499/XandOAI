from math import sqrt, log, e
import random as r
import json


datafolderprefix = "C:\\Users\\Thomas\\Documents\\XandOdata*.json"


def fetch_json(j):  # converts json string to dictionary
    import json
    temp1 = json.load(j)
    return_val = dict()
    for item in temp1:
        _ = list(eval(item))
        return_val[_[0]] = eval(item)[_[0]]
    return return_val


def fetchfromfile(filename):  # converts file with json string to dictionary
    with open(filename) as file:
        return_value = fetch_json(file)
    return return_value


def fetchfromdata(number):
    with open(f"C:\\Users\\Thomas\\Documents\\XandOdata{number}.json") as file:
        return_value = fetch_json(file)
    return return_value


def find_children(parentname):
    children = []
    for potential_child in range(1, 10):
        if str(potential_child) not in parentname:
            children.append(parentname + str(potential_child))
    return children


def getdata(node):
    return fetchfromfile(datafolderprefix.replace('*', str(len(node))))[node]


def getchilddata(parent):
    child_file = fetchfromfile(datafolderprefix.replace('*', str(len(parent)+1)))
    return_dict = dict()
    for child in child_file:
        if child.startswith(parent):
            return_dict[child] = child_file[child]
    return return_dict


def keys_with_top_values(my_dict):
    return [key for (key, value) in my_dict.items() if value == max(my_dict.values())]


def choose_child(parent):
    roundnum = len(parent) + 1
    boarddata = fetchfromfile(datafolderprefix.replace('*', str(roundnum)))
    win_ratio = 0
    best_child = dict()
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
            templog = log(getdata(parent)['p'], e)
            choice_factor = win_ratio + c * sqrt(templog/plays)
        choice_list[child] = choice_factor

    best_child = r.choice(keys_with_top_values(choice_list))

    return best_child


def have_turn(board_state: str, bot: bool):
    if bot:
        roundnum = len(board_state) + 1
        return choose_child(board_state)
    else:
        turn = input('>>> ')
        return turn


def play_simulation():
    first = r.choice([True, False])
    if first:
        pass


c = sqrt(2)
simulations = 1

print(have_turn('1', True))
