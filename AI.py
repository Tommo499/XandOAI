# import random as r
import json
from math import sqrt

c = sqrt(2)

def choose_child(round, parent):
    with open(f"C:\\Users\\twach\\PycharmProjects\\XandO\\XandOdata{round}.json") as data:
        board = json.load(data)
        boarddata = dict()
        for thing in board:
            _ = list(eval(thing))
            boarddata[_[0]] = eval(thing)[_[0]]
        print(boarddata)
    # with relevant data open, find children and their data
    """
    for child in children:
        wins = 0
        plays = 0
        if plays == 0:
            win_ratio = 0
        else:
            win_ratio = wins / plays
         """

    return 0


choose_child(1, "")
