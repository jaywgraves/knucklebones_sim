def description():
    return """find any open column on my board and put the die in it"""

def play(die, me, opp):
    # 'a' and 'b' can refer to either p1 or p2 based
    # on who is playing this turn
    return me.choose(me.board.avail_columns())