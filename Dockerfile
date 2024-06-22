# syntax=docker/dockerfile:1

FROM --platform=linux/amd64 python:3.12-rc-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
ENV MINIO_ENDPOINT=minio:9000
ENV SQLALCHEMY_DATABASE_URI=sqlite:///project.db

RUN flask db stamp head
RUN flask db migrate
RUN flask db upgrade

EXPOSE 5000

CMD [ "python3", "run.py" ]