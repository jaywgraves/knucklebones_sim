
def play(die, a, b):
    # 'a' and 'b' can refer to either p1 or p2 based
    # on who is playing this turn
    # find any open column on my board and put the die in it
    return a.choose(a.board.avail_columns())