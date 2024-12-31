create table strategy as
select * from read_json_auto('data/strategies.json');

create table turns as
select *
from
    read_csv('data/*_turns.csv', names = [game_nbr, round_cnt, turn_cnt, player_name, strat, player_seed, die, play_col, result, p1_score, p1_cnt, p2_score, p2_cnt]);

create table games as with
p1 as (select
    game_nbr,
    strat,
    player_seed
from turns
where round_cnt = 1 and turn_cnt = 1),
p2 as (select
    game_nbr,
    strat,
    player_seed
from turns
where round_cnt = 1 and turn_cnt = 2)
select
    p1.game_nbr,
    p1.strat as p1_strat,
    p1.player_seed as p1_seed,
    p2.strat as p2_strat,
    p2.player_seed as p2_seed
from p1 inner join p2 on (p1.game_nbr = p2.game_nbr)
order by p1.game_nbr;
