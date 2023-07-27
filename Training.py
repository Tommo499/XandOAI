from AI import *


def writeresults(result_dict: dict):
    for state, result in result_dict.items():
        temp = []
        for end in range(1, len(state) + 1):
            gamescore = list()
            cur.execute('SELECT * FROM data WHERE name = ?', (dbname(state[:end]),))
            gamescore = cur.fetchone()
            if result == 0:
                newgamescore = (gamescore[0], gamescore[1] + 0.5, gamescore[2] + 1)
                cur.execute("UPDATE data SET wins = ?, plays = ? WHERE name = ?", (newgamescore[1],) + (newgamescore[2],) + (newgamescore[0],))
            else:
                if end % 2 == result % 2:  # player wins
                    newgamescore = (gamescore[0], gamescore[1] + 1, gamescore[2] + 1)
                    print((newgamescore[1:],) + (newgamescore[0],))
                    cur.execute("UPDATE data SET wins = ?, plays = ? WHERE name = ?", (newgamescore[1],) + (newgamescore[2],) + (newgamescore[0],))
                elif end % 2 != result % 2:  # player loses
                    newgamescore = (gamescore[0], gamescore[1], gamescore[2] + 1)
                    print((newgamescore[1:],) + (newgamescore[0],))
                    cur.execute("UPDATE data SET wins = ?, plays = ? WHERE name = ?", (newgamescore[1],) + (newgamescore[2],) + (newgamescore[0],))


def train(rounds: int):
    results = dict()
    for n in range(rounds):
        results = dict()
        result, gamestate = playsimulation(True)
        results[gamestate] = result

    writeresults(results)
    con.commit()

train(1000)
