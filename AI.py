from math import sqrt

c = sqrt(2)
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


def find_children(parentname):
    children = []
    for potential_child in range(1, 10):
        if str(potential_child) not in parentname:
            children.append(parentname + str(potential_child))
    return children


def getchilddata(parent):
    child_file = fetchfromfile(datafolderprefix.replace('*', str(len(parent)+1)))
    for child in child_file:
        if not child.startswith(parent):
            child_file.pop(child)
    return child_file


def choose_child(roundnum, parent):
    boarddata = fetchfromfile(datafolderprefix.replace('*', str(roundnum)))
    print(getchilddata('1'))

    for child in find_children(parent):
        wins = 0
        plays = 0
        if plays == 0:
            win_ratio = 0
        else:
            win_ratio = wins / plays

    return 0


choose_child(1, "")
