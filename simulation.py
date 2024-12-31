import time
import datetime
import json
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

def get_strategy_info(strategy_info, player):
    name = player.strategy_name
    desc = player.strategy_description
    if name not in strategy_info:
        strategy_info[name] = {"name": name, "description": desc}

if __name__ == '__main__':
    all_turns = []
    strategy_info = {}
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
        get_strategy_info(strategy_info, p1)
        p2 = knucklebones.Player('p2', get_seed(beg_seed, end_seed), "jerk")
        get_strategy_info(strategy_info, p2)
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
    with open(os.path.join(data_dir, 'strategies.json'),'w') as f:
        for s in strategy_info.values():
            f.write(json.dumps(s) + "\n")
    end = time.time()

    print("elapsed seconds", end-start)
