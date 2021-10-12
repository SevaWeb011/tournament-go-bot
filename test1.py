import os

os.system("docker run --env HOST=194.32.248.108  --env DATABASE=tournament_go --env USER=foilv --env PASSWORD={{ PASSWORD }} --env BOT={{ BOT }} foilv/tournaments_go:bot15")