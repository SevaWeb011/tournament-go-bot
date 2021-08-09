import requests
from bs4 import BeautifulSoup

#url = 'https://gofederation.ru/tournaments/' # url страницы
#r = requests.get(url)
#with open('test1.html', 'w') as output_file:
 #output_file.write(r.text)

#r.close()


def compare(test, test1):
    with open(test,'r') as f:
        d=set(f.readlines())
        soup = BeautifulSoup(d, 'lxml')
        print(soup.find("table", id="tbody"))


    with open(test1,'r') as f:
        e=set(f.readlines()) 
        soup1 = BeautifulSoup(e, 'lxml')
        print(soup1.find("table", id="tbody"))

    open('difference.html','w').close() #Create the file

    with open('difference.html','a') as f:
        for line in list(e-d):
           f.write(line)
          
if __name__ == '__main__':
  compare("soup", "soup1")


  #contents = f.read()
 
    #soup = BeautifulSoup(contents, 'lxml')
 
    #print(soup.find("ul", attrs={ "id" : "mylist"}))
    #print(soup.find("ul", id="mylist"))
