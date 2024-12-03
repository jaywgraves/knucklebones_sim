import random
import collections

class Game(object):

    def __init__(self, p1, p2, show_output):
        self.p1 = p1
        self.p2 = p2

    def check_for_win(self):
        # one of the boards must be full
        # but the player without the full board could still be the winner
        p1_score = self.p1.board.score()
        p2_score = self.p2.board.score()
        p1_full = self.p1.board.full()
        p2_full = self.p2.board.full()
        winning_player = ''
        if p1_full or p2_full:
            if p1_score == p2_score:
                winning_player = 'tie'
            elif p1_score > p2_score:
                winning_player = 'p1'
            else:
                winning_player = 'p2'
        return winning_player, p1_score, p2_score

    def play(self, game_nbr):
        turn_cnt = 0
        stats = []
        while True:
            turn_cnt += .5
            die = self.p1.roll()
            play_col = self.p1.strategy(die, self.p1, self.p2)
            success = self.p1.board.place(die, play_col)
            if success:
                self.p2.board.remove(die, play_col)
            else:
                print("strategy made an invalid suggestion")
            result, p1_score, p2_score = self.check_for_win()
            stats.append((game_nbr, turn_cnt, result, p1_score, p2_score))
            if result:
                print("result", result, "p1", p1_score, "p2", p2_score)
                break
            turn_cnt += .5
            die = self.p2.roll()
            play_col = self.p2.strategy(die, self.p2, self.p1)
            success = self.p2.board.place(die, play_col)
            if success:
                self.p1.board.remove(die, play_col)
            else:
                print("strategy made an invalid suggestion")
            result, p1_score, p2_score = self.check_for_win()
            stats.append((game_nbr, turn_cnt, result, p1_score, p2_score))
            if result:
                print("result", result, "p1", p1_score, "p2", p2_score)
                break
            print("turn summary", turn_cnt, p1_score, p2_score)
            # temp debugging
            if turn_cnt > 10:
                break
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

    def full(self):
        return not self.avail_columns()

    def avail_columns(self):
        cols = self._columns()
        available = [i for i,c in enumerate(cols) if 0 in c]
        return available


class Player(object):

    def __init__(self, name, seed, strategy):
        self.name = name
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
    return a.choose(a.board.avail_columns())

def first_available(die, a, b):
    # 'a' and 'b' can refer to either p1 or p2 based
    # on who is playing this turn
        desc = 'first available'
        a_score = a.board.score()
        b_score = b.board.score()
        # find first open column on my board and put the die in it
        return a.board.avail_columns()[0]