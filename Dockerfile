# syntax=docker/dockerfile:1

FROM --platform=linux/amd64 python:3.12-rc-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN flask db migrate
RUN flask db upgrade

EXPOSE 5000

CMD [ "python3", "run.py" ]