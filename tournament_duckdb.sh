# make this find the next tournament.nn.duckdb file
# instead of using a parameter
duckdb -c '.read tournament_duckdb.sql' $1
rm data/*_turns.csv