import os

def size():
    file_size = os.path.getsize("BOT/old.html")
    if int(file_size) != 0:
        print(file_size)
    else:
        print("ERROR")

if __name__ == '__main__':
    size()
