def description():
    return """place die only favoring making combos:
figure out if any of my available columns has
the matching die and put it in the one with
the most of that die."""

def play(die, me, opp):
    my_cols = me.board._columns()
    my_avail = me.board.avail_columns()
    max_cnt = 0
    max_cnt_col = []
    for c in my_avail:
        cnt = my_cols[c].count(die)
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
