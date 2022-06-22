#--- Variables
places = {'p' + str(n): str(n) for n in range(1, 10)}

board = f" {places['p7']} ███ {places['p8']} ███ {places['p9']} \n" \
        f"███████████████\n" \
        f" {places['p4']} ███ {places['p5']} ███ {places['p6']} \n" \
        f"███████████████\n" \
        f" {places['p1']} ███ {places['p2']} ███ {places['p3']}"
turn = 'X'
won = False
game = False
go = ''
winConditions = ((1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7))


def update():
    global places
    if go.isdigit() and len(str(go)) == 1:
        if places['p' + go] == go:
            places['p' + go] = turn
            change_turn(turn)
        else:
            print('Try again.')
    else:
        print('Try again.')


def change_turn(a):
    global turn
    if a == 'X':
        turn = 'O'
    else:
        turn = 'X'


def check_for_win():
    global won
    for triple in winConditions:
        if places['p' + str(triple[0])] == places['p' + str(triple[1])] == places['p' + str(triple[2])] and places['p' + str(triple[1])] != str(triple[1]):
            print(places['p' + str(triple[0])] + ' wins')
            won = True
            quit(0)
    else:
        won = False


def play():
    global go
    global board
    go = input('>>>')
    update()

    board = f" {places['p7']} ███ {places['p8']} ███ {places['p9']} \n" \
        f"███████████████\n" \
        f" {places['p4']} ███ {places['p5']} ███ {places['p6']} \n" \
        f"███████████████\n" \
        f" {places['p1']} ███ {places['p2']} ███ {places['p3']}" \

    print(board, sep='\n')
    check_for_win()


print(board)
while not won:
    play()
    used = False
    for _ in range(1, 10):
        if places['p' + str(_)] == str(_):
            used = True

    if not used:
        print('Tie')
        quit(0)
