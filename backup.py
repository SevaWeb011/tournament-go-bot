import os
import time

while True:
    def backup():
        try:
            os.system("mysqldump -u root tournament_go > /tmp/tournament_go.sql")
        except Exception as e:
            print(e) 
    time.sleep(300) # 5мин
