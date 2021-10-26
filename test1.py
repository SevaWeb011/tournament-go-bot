from datetime import datetime

def date(): 
    date = datetime.now().date()
    try:           
        format_string = "%Y-%m-%d"
        today = datetime.strptime(str(date), format_string).strftime("%Y-%m-%d")
        print(today)
    except TypeError as e:
        print(e)

if __name__ == '__main__':
    date()

