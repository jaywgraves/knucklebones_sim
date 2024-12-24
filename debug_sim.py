import knucklebones

def sim_game(game_nbr, p1_seed, p1_strat, p2_seed, p2_strat):
    p1 = knucklebones.Player('p1', p1_seed, p1_strat)
    p2 = knucklebones.Player('p2', p2_seed, p2_strat)

    g = knucklebones.Game(p1, p2, show_output=True)
    stats = g.play(game_nbr)

if __name__ == '__main__':
    #sim_game(1, 565529, 'random_play', 831366,'first_available')

    #sim_game(6563, 21656, 'random_play', 536434,'first_available')
    #sim_game(7947, 995409, 'random_play', 995409,'first_available')

    sim_game(1, 1001, 'jerk', 831366, 'random_play')