FROM python:3.8.2-slim-buster

ARG HOST 
ARG DATABASE 
ARG USER 
ARG PASSWORD 
ARG BOT

RUN pip3 install python-telegram-bot pythonping pyyaml BeautifulSoup4 pytelegrambotapi mysql-connector-python lxml

RUN mkdir /app

COPY ./BOT /app

WORKDIR /app

ENTRYPOINT ["python"]

CMD ["bot.py"] 
