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
    all_turns = []
    total_runs = 10000
    checkpoint = 10000
    show_output = False
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
        p1 = knucklebones.Player('p1', get_seed(beg_seed, end_seed), "jerk")
        p2 = knucklebones.Player('p2', get_seed(beg_seed, end_seed), "jerk")

        g = knucklebones.Game(p1, p2, show_output=show_output)
        turns = g.play(game_nbr)
        all_turns.extend(turns)
        if (game_nbr) % checkpoint == 0:
            filename = format(i+1, "08d") + '_turns.csv'
            print("saving checkpoint", filename, datetime.datetime.isoformat(datetime.datetime.now()))
            with open(os.path.join(data_dir, filename),'w') as f:
                for s in all_turns:
                    f.write(",".join(str(x) for x in s) + "\n")
            all_turns.clear()
    end = time.time()

    print("elapsed seconds", end-start)
