import random
import collections

class Game(object):

    def __init__(self, p1, p2, show_output):
        self.p1 = p1
        self.p2 = p2
        self.show_output = show_output

    def check_for_win(self):
        # one of the boards must be full
        # but the player without the full board could still be the winner
        p1_score = self.p1.board.score()
        p2_score = self.p2.board.score()
        p1_empty_cnt = self.p1.board.empty_count()
        p2_empty_cnt = self.p2.board.empty_count()

        winning_player = ''
        if p1_empty_cnt == 0 or p2_empty_cnt == 0:
            if p1_score == p2_score:
                winning_player = 'tie'
            elif p1_score > p2_score:
                winning_player = 'p1'
            else:
                winning_player = 'p2'
        return winning_player, p1_score, 9 - p1_empty_cnt, p2_score, 9 - p2_empty_cnt

    def play(self, game_nbr):
        turn_cnt = 0
        round_cnt = 0
        game_over = False
        stats = []
        while True:
            round_cnt += 1
            for pcurr,pother in ((self.p1, self.p2), (self.p2, self.p1)):
                turn_cnt += 1
                die = pcurr.roll()
                strat, play_col = pcurr.strategy(die, pcurr, pother)
                if self.show_output:
                    print(f"{pcurr.name} rolled:{die}  picked column:{play_col+1}")
                success = pcurr.board.place(die, play_col)
                if success:
                    pother.board.remove(die, play_col)
                else:
                    print(f"{pcurr.name} strategy {strat} made an invalid suggestion")
                    print(stats)
                    raise SystemExit
                result, p1_score, p1_cnt, p2_score, p2_cnt = self.check_for_win()
                stats.append((game_nbr, round_cnt, turn_cnt, pcurr.name, strat, pcurr.seed, die, play_col, result, p1_score, p1_cnt, p2_score, p2_cnt))
                if result:
                    if self.show_output:
                        print(f"result:{result} p1={p1_score} p2={p2_score}")
                    game_over = True
                    break  # round iteration
            # end round
            if self.show_output:
                self.p2.board.show(self.p2.name, reverse=True)
                print('     -----')
                self.p1.board.show(self.p1.name)
                if game_over:
                    summary_type = 'final summary total rounds:'
                else:
                    summary_type = 'round summary:'
                print(f"{summary_type}{round_cnt} p1={p1_score} p2={p2_score}")
                print()
            if game_over:
                break  # whole game loop
        return stats


class Board(object):

    def __init__(self, values=None):
        if not values:
            self.data = [0]*9
        else:
            self.data = values

    def place(self, die, col_idx):
        cols = self._columns()
        new_col = []
        for v in cols[col_idx]:
            if v:
                new_col.append(v)
            else:
                new_col.append(die)
                break
        new_col.extend([0]*3)
        new_col = new_col[:3]
        cols[col_idx] = new_col
        self.to_list(*cols)
        return True

    def remove(self, die, col_idx):
        cols = self._columns()
        new_col = []
        for v in cols[col_idx]:
            if v != die:
                new_col.append(v)
        new_col.extend([0]*3)
        new_col = new_col[:3]
        cols[col_idx] = new_col
        self.to_list(*cols)
        return True

    def score(self):
        cnt = collections.defaultdict(int)
        cols = self._columns()
        score_1 = self._score_column(cnt, cols[0])
        score_2 = self._score_column(cnt, cols[1])
        score_3 = self._score_column(cnt, cols[2])
        return score_1 + score_2 + score_3

    def _columns(self):
        col_1 = self.data[0:3]
        col_2 = self.data[3:6]
        col_3 = self.data[6:9]
        return [col_1, col_2, col_3]

    def to_list(self, col_1, col_2, col_3):
        self.data[0:3] = col_1
        self.data[3:6] = col_2
        self.data[6:9] = col_3

    def _score_column(self, cnt, col):
        cnt.clear()
        for pip in col:
            cnt[pip] += 1
        score = 0
        for pip,nbr in cnt.items():
            if nbr == 1:
                score += pip
            elif nbr == 2:
                score += (pip * 4)
            elif nbr == 3:
                score += (pip * 9)
        return score

    def empty_count(self):
        return self.data.count(0)

    def avail_columns(self):
        cols = self._columns()
        available = [i for i,c in enumerate(cols) if 0 in c]
        return available

    def show(self, player_name, reverse=False):
        cols = self._columns()
        if reverse:
            cols = [list(reversed(c)) for c in cols]
        row = 0
        for a,b,c in zip(*cols):
            if a == 0: a = '-'
            if b == 0: b = '-'
            if c == 0: c = '-'
            if row == 1:
                prefix = f"{player_name}  "
            else:
                prefix = "    "
            row += 1
            print(prefix, a, b, c)



class Player(object):

    def __init__(self, name, seed, strategy):
        self.name = name
        self.seed = seed
        self.rand_dice = random.Random(seed)
        self.rand_decision = random.Random(seed)
        if strategy:
            self.strategy = strategy
        else:
            self.strategy = random_play
        self.board = Board()

    def roll(self):
        return self.rand_dice.randint(1,6)

    def choose(self, choices=[0,1]):
        return self.rand_decision.choice(choices)


def random_play(die, a, b):
    # 'a' and 'b' can refer to either p1 or p2 based
    # on who is playing this turn
    desc = 'random play'
    a_score = a.board.score()
    b_score = b.board.score()
    # find any open column on my board and put the die in it
    return desc, a.choose(a.board.avail_columns())

def first_available(die, a, b):
    # 'a' and 'b' can refer to either p1 or p2 based
    # on who is playing this turn
    desc = 'first available'
    a_score = a.board.score()
    b_score = b.board.score()
    # find first open column on my board and put the die in it
    return desc, a.board.avail_columns()[0]