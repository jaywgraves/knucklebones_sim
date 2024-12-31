def description():
    return """find first open column on my board and put the die in it"""

def play(die, me, opp):
    return me.board.avail_columns()[0]