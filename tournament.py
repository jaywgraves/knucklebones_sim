import time
import datetime
import random
import os
import itertools
import knucklebones

seeds_used = set()
def get_seed(start,end,seeds_used=seeds_used):
    seed = random.randint(start, end)
    while seed in seeds_used:
        seed = random.randint(start, end)
    seeds_used.add(seed)
    return seed

if __name__ == '__main__':
    strategies = ('random_play', 'first_available', 'jerk', 'piggy')
    pairs = list(itertools.product(strategies ,repeat=2))
    total_games_per_matchup = 10000
    show_output = False
    data_dir = 'data'
    beg_seed = 1
    end_seed = total_games_per_matchup * 100 * len(pairs)
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    if os.listdir(data_dir):
        print(data_dir, "not empty.  aborting")
        raise SystemExit
    start = time.time()
    game_nbr = 0
    for strat1,strat2 in pairs:
        print(f'{strat1} vs {strat2}')
        all_stats = []
        for i in range(total_games_per_matchup):
            game_nbr += 1
            p1 = knucklebones.Player('p1', get_seed(beg_seed, end_seed), strat1)
            p2 = knucklebones.Player('p2', get_seed(beg_seed, end_seed), strat2)

            g = knucklebones.Game(p1, p2, show_output=show_output)
            stats = g.play(game_nbr)
            all_stats.extend(stats)
        filename = format(game_nbr, "08d") + '_stats.csv'
        print("saving stats", filename)
        with open(os.path.join(data_dir, filename),'w') as f:
            for s in all_stats:
                f.write(",".join(str(x) for x in s) + "\n")
        all_stats.clear()
        print("elapsed seconds", time.time()-start)
        print()
    end = time.time()
    print("total elapsed seconds", end-start)
