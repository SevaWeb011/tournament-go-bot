FROM python:3.8.2-slim-buster

ARG MYSQL_DATABASE
ARG MYSQL_USER
ARG MYSQL_PASSWORD

ENV MYSQL_DATABASE=tournament_go
ENV MYSQL_USER=foilv
ENV MYSQL_PASSWORD=${PASSWORD}

RUN pip3 install python-telegram-bot pythonping pyyaml BeautifulSoup4 pytelegrambotapi mysql-connector-python lxml

RUN mkdir /app

COPY ./BOT /app

WORKDIR /app

ENTRYPOINT ["python"]

CMD ["bot.py"] 
