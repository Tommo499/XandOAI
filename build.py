# A small script which populates 'data.db' using the data in 'data.txt'
# For some reason, when 'data.db' is downloaded, it erases all of the data
# Thomas Wachmer 2022

def writeTableToFile():
    import sqlite3 as sql
    con = sql.connect('data.db')
    con.cursor()
    data = []

    table = con.execute('SELECT * FROM data')

    for row in table:
        data.append(row)

    with open('data.txt', 'w') as file:
        for line in data:
            file.write(f'{int(line[0])} {line[1]} {line[2]}\n')


def writeFileToTable():
    import sqlite3
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='data';")
    if len(cur.fetchone()) == 1:  # Check to see if table 'data' exists, if so, delete it
        cur.execute('DROP TABLE data')
    cur.execute("CREATE TABLE data (name text, wins real, plays integer)")

    data = []
    with open('data.txt', 'r') as file:
        for line in file:
            data.append((line[:-1].split(' ')))  # trim off newline and split by spaces
    data = sorted(data, key=lambda row: len(row[0]))  # sort by first item in row
    upto = 0
    for row in data:
        upto += 1
        print(f"{upto}/5477")  # I should make this dynamic but it will do for now
        row[1] = float(row[1])
        row[2] = int(row[2])
        cur.execute('INSERT INTO data VALUES (?, ?, ?)', tuple(row))
    con.commit()


# Add function call below (writeFileToTable for filling out the database,
# or writeTableToFile for backups or transfers)

# Make sure the database file is 'data.db' with a table called 'data'
# Make sure 'data.txt' has one entry per row and the entries are separated by single spaces
# An entry has the name first, the wins (float) then the plays (int)

