import time
import datetime
import random
import os
import knucklebones

seeds_used = set()
def get_seed(start,end,seeds_used=seeds_used):
    seed = random.randint(start, end)
    while seed in seeds_used:
        seed = random.randint(start, end)
    seeds_used.add(seed)
    return seed

if __name__ == '__main__':
    all_stats = []
    total_runs = 1
    checkpoint = 100
    show_output = True
    data_dir = 'data'
    beg_seed = 1
    end_seed = total_runs * 100
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    if os.listdir(data_dir):
        print(data_dir, "not empty.  aborting")
        raise SystemExit
    start = time.time()
    for i in range(total_runs):
        game_nbr = i+1
        p1 = knucklebones.Player('x', get_seed(beg_seed, end_seed), knucklebones.random_play)
        p2 = knucklebones.Player('y', get_seed(beg_seed, end_seed), knucklebones.random_play)

        g = knucklebones.Game(p1, p2, show_output=show_output)
        stats = g.play(game_nbr)
        all_stats.extend(stats)
        continue   # temporary
        if (game_nbr) % checkpoint == 0:
            filename = format(i+1, "08d") + '_stats.csv'
            print("saving checkpoint", filename, datetime.datetime.isoformat(datetime.datetime.now()))
            with open(os.path.join(data_dir, filename),'w') as f:
                for s in all_stats:
                    f.write(",".join(str(x) for x in s) + "\n")
            all_stats.clear()
    end = time.time()

    print("elapsed seconds", end-start)
