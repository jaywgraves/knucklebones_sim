def description():
    return """place my die only favoring knocking out other player:
using my available columns, figure out which opponent's column
has the most of my die."""

def play(die, me, opp):
    opp_cols = opp.board._columns()
    my_avail = me.board.avail_columns()
    max_cnt = 0
    max_cnt_col = []
    for c in my_avail:
        cnt = opp_cols[c].count(die)
        if not max_cnt:
            max_cnt = cnt
            max_cnt_col.append(c)
        else:
            if cnt == max_cnt:
                max_cnt_col.append(c)
            elif cnt > max_cnt:
                max_cnt = cnt
                max_cnt_col.clear()
                max_cnt_col.append(c)
    if max_cnt == 0:
        choice = me.choose(my_avail)
    else:
        choice = me.choose(max_cnt_col)
    return choice
