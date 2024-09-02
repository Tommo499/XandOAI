# Thomas Wachmer 2022
from math import ceil
import sqlite3

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

if __name__ == "__main__":    
    try:
        con = sqlite3.connect('data.db')
    except NameError:
        with open("data.db", "x") as file:
            pass
        con = sqlite3.connect('data.db')
    cur = con.cursor()
    #cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='data';")
    #if len(cur.fetchone()) == 1:  # Check to see if table 'data' exists, if so, delete it
    #    cur.execute('DROP TABLE data')

    # Going to assume the file is empty
    cur.execute("CREATE TABLE data (name text, wins real, plays integer)")


    spots = '123456789'
    writelist = []

    for leng in range(1, 10):
        for branch in permutations(spots, leng): # Terribly inefficient but it will work for now
            if not redundant(branch):
                p1 = ''.join(sorted(list(branch[0::2])))
                p2 = ''.join(sorted(list(branch[1::2])))
                temp = (p1 + p2, 0, 0)
                if temp not in writelist:
                    writelist.append(temp)

    cur.executemany("insert into data values (?, ?, ?)", writelist)


    con.commit()

