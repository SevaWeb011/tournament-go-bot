FROM python:buster

RUN pip3 install python-telegram-bot pythonping pyyaml BeautifulSoup4 pytelegrambotapi mysql-connector-python lxml

RUN mkdir /app

COPY . /app

WORKDIR /app

ENTRYPOINT ["python"]

CMD ["bot.py"]