
def play(die, a, b):
    # 'a' and 'b' can refer to either p1 or p2 based
    # on who is playing this turn
    # place my die favoring combos
    my_cols = a.board._columns()
    my_avail = a.board.avail_columns()
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
        choice = a.choose(my_avail)
    else:
        choice = a.choose(max_cnt_col)
    return choice
