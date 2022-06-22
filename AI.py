# import random as r
from pprint import pprint
import json
from math import sqrt

c = sqrt(2)
"""
with open("C:\\Users\\twach\\PycharmProjects\\XandO\\XandOdata1.json") as file:
    for line in file:
        pprint(line)
"""

def choose_child(round, parent):
    with open(f"C:\\Users\\twach\\PycharmProjects\\XandO\\XandOdata{round}.json") as data:
        board = json.load(data)
        print(board)

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