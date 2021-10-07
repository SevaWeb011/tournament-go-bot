import os

def backup():
    try:
        os.system("mysqldump -u root tournament_go > /appBot/tournament_go.sql")
    except Exception as e:
        print(e) 
