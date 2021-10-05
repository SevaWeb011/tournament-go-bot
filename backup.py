import os
import time

def backup():
    try:
        os.system("mysqldump -u root tournament_go > /tmp/tournament_go.sql")
    except Exception as e:
        print(e) 
