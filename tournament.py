import time
import json
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

def get_strategy_info(strategy_info, player):
    name = player.strategy_name
    desc = player.strategy_description
    if name not in strategy_info:
        strategy_info[name] = {"name": name, "description": desc}

if __name__ == '__main__':
    strategies = ('random_play', 'first_available', 'jerk', 'piggy')
    strategy_info = {}
    pairs = list(itertools.product(strategies ,repeat=2))
    total_games_per_matchup = 100
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
        all_turns = []
        for i in range(total_games_per_matchup):
            game_nbr += 1
            p1 = knucklebones.Player('p1', get_seed(beg_seed, end_seed), strat1)
            get_strategy_info(strategy_info, p1)
            p2 = knucklebones.Player('p2', get_seed(beg_seed, end_seed), strat2)
            get_strategy_info(strategy_info, p2)

            g = knucklebones.Game(p1, p2, show_output=show_output)
            turns = g.play(game_nbr)
            all_turns.extend(turns)
        filename = format(game_nbr, "08d") + '_turns.csv'
        print("saving turn data", filename)
        with open(os.path.join(data_dir, filename),'w') as f:
            for s in all_turns:
                f.write(",".join(str(x) for x in s) + "\n")
        all_turns.clear()
        print("elapsed seconds", time.time()-start)
        print()
    print("saving strategy data", filename)
    with open(os.path.join(data_dir, 'strategies.json'),'w') as f:
        for s in strategy_info.values():
            f.write(json.dumps(s) + "\n")
    end = time.time()
    print("total elapsed seconds", end-start)
