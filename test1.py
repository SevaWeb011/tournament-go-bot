import os

def docker_run():
    try:
        os.system("docker run --env HOST=194.32.248.108  --env DATABASE=tournament_go --env USER=foilv --env PASSWORD=${{ secrets.PASS_ROOT }} --env BOT=${{ secrets.BOT }} foilv/tournaments_go:bot15")
    except Exception as e:
        print(e) 